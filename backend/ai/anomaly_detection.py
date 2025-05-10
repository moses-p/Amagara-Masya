import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
import joblib
import logging
from datetime import datetime, timedelta
from django.conf import settings
from django.db.models import Avg, Count, Q
from ..models import Child, Anomaly, Activity, Location, Device, Note

logger = logging.getLogger(__name__)

class AnomalyDetectionSystem:
    def __init__(self):
        self.model = None
        self.scaler = None
        self.load_model()

    def load_model(self):
        """Load the trained model and scaler"""
        try:
            self.model = joblib.load(settings.ANOMALY_MODEL_PATH)
            self.scaler = joblib.load(settings.ANOMALY_SCALER_PATH)
        except Exception as e:
            logger.error(f"Error loading anomaly model: {str(e)}")
            self.model = IsolationForest(contamination=0.1, random_state=42)
            self.scaler = StandardScaler()

    def detect_anomalies(self, child):
        """Detect anomalies for a child. This method aggregates all rule-based and ML-based anomaly checks."""
        try:
            anomalies = []

            # Location anomalies
            location_anomalies = self._detect_location_anomalies(child)
            if location_anomalies:
                anomalies.extend(location_anomalies)

            # Activity anomalies
            activity_anomalies = self._detect_activity_anomalies(child)
            if activity_anomalies:
                anomalies.extend(activity_anomalies)

            # Device anomalies
            device_anomalies = self._detect_device_anomalies(child)
            if device_anomalies:
                anomalies.extend(device_anomalies)

            # Note anomalies
            note_anomalies = self._detect_note_anomalies(child)
            if note_anomalies:
                anomalies.extend(note_anomalies)

            # --- Additional Rules ---
            # 1. Time-of-day movement (e.g., movement at night)
            tod_anomalies = self._detect_time_of_day_movement(child)
            if tod_anomalies:
                anomalies.extend(tod_anomalies)

            # 2. Device tampering (e.g., device removed or reset)
            tamper_anomalies = self._detect_device_tampering(child)
            if tamper_anomalies:
                anomalies.extend(tamper_anomalies)

            # 3. Repeated missed activities (e.g., 3+ missed in a row)
            repeat_missed = self._detect_repeated_missed_activities(child)
            if repeat_missed:
                anomalies.extend(repeat_missed)

            # Save detected anomalies
            for anomaly in anomalies:
                Anomaly.objects.create(
                    child=child,
                    anomaly_type=anomaly['type'],
                    description=anomaly['description'],
                    severity=anomaly['severity'],
                    timestamp=datetime.now()
                )

            return anomalies
        except Exception as e:
            logger.error(f"Error detecting anomalies for child {child.id}: {str(e)}")
            return []

    def _detect_location_anomalies(self, child):
        """Detect location-based anomalies"""
        anomalies = []
        try:
            # Get recent locations
            recent_locations = Location.objects.filter(
                child=child,
                timestamp__gte=datetime.now() - timedelta(days=7)
            ).order_by('timestamp')

            if not recent_locations:
                return anomalies

            # Check for missing location updates
            expected_updates = 24 * 7  # hourly updates for 7 days
            actual_updates = recent_locations.count()
            if actual_updates < expected_updates * 0.8:  # Less than 80% of expected updates
                anomalies.append({
                    'type': 'location',
                    'description': f'Missing location updates: {actual_updates}/{expected_updates}',
                    'severity': 'high'
                })

            # Check for unusual movement patterns
            locations_array = np.array([(loc.latitude, loc.longitude) for loc in recent_locations])
            if len(locations_array) > 1:
                # Calculate movement speed
                distances = np.sqrt(np.sum(np.diff(locations_array, axis=0)**2, axis=1))
                times = np.array([(loc.timestamp - recent_locations[i].timestamp).total_seconds() 
                                for i, loc in enumerate(recent_locations[1:])])
                speeds = distances / times

                # Detect unusual speeds
                if np.any(speeds > 100):  # Speed threshold in km/h
                    anomalies.append({
                        'type': 'location',
                        'description': 'Unusual movement speed detected',
                        'severity': 'high'
                    })

                # Detect unusual locations
                if np.any(recent_locations.filter(is_unusual=True)):
                    anomalies.append({
                        'type': 'location',
                        'description': 'Unusual locations detected',
                        'severity': 'high'
                    })

            return anomalies
        except Exception as e:
            logger.error(f"Error detecting location anomalies: {str(e)}")
            return anomalies

    def _detect_activity_anomalies(self, child):
        """Detect activity-based anomalies"""
        anomalies = []
        try:
            # Get recent activities
            recent_activities = Activity.objects.filter(
                child=child,
                timestamp__gte=datetime.now() - timedelta(days=7)
            )

            if not recent_activities:
                return anomalies

            # Check for missed activities
            missed_activities = recent_activities.filter(status='missed')
            if missed_activities.count() > 0:
                anomalies.append({
                    'type': 'activity',
                    'description': f'Missed activities: {missed_activities.count()}',
                    'severity': 'medium'
                })

            # Check for unusual completion times
            completed_activities = recent_activities.filter(status='completed')
            if completed_activities.count() > 0:
                completion_times = [act.completion_time for act in completed_activities if act.completion_time]
                if completion_times:
                    avg_time = np.mean(completion_times)
                    std_time = np.std(completion_times)
                    unusual_times = [t for t in completion_times if abs(t - avg_time) > 2 * std_time]
                    if unusual_times:
                        anomalies.append({
                            'type': 'activity',
                            'description': f'Unusual activity completion times: {len(unusual_times)}',
                            'severity': 'low'
                        })

            return anomalies
        except Exception as e:
            logger.error(f"Error detecting activity anomalies: {str(e)}")
            return anomalies

    def _detect_device_anomalies(self, child):
        """Detect device-based anomalies"""
        anomalies = []
        try:
            devices = Device.objects.filter(child=child)

            if not devices:
                return anomalies

            # Check for device connectivity issues
            for device in devices:
                if device.last_seen:
                    time_since_last_seen = (datetime.now() - device.last_seen).total_seconds()
                    if time_since_last_seen > 3600:  # No updates in last hour
                        anomalies.append({
                            'type': 'device',
                            'description': f'Device {device.device_token[:10]}... disconnected',
                            'severity': 'high'
                        })

                # Check for battery issues
                if device.battery_level < 20:
                    anomalies.append({
                        'type': 'device',
                        'description': f'Low battery on device {device.device_token[:10]}...',
                        'severity': 'medium'
                    })

                # Check for signal strength
                if device.signal_strength < 0.3:
                    anomalies.append({
                        'type': 'device',
                        'description': f'Poor signal strength on device {device.device_token[:10]}...',
                        'severity': 'medium'
                    })

            return anomalies
        except Exception as e:
            logger.error(f"Error detecting device anomalies: {str(e)}")
            return anomalies

    def _detect_note_anomalies(self, child):
        """Detect note-based anomalies"""
        anomalies = []
        try:
            # Get recent notes
            recent_notes = Note.objects.filter(
                child=child,
                created_at__gte=datetime.now() - timedelta(days=30)
            )

            if not recent_notes:
                return anomalies

            # Check for negative sentiment
            negative_notes = recent_notes.filter(sentiment_score__lt=0.3)
            if negative_notes.count() > 0:
                anomalies.append({
                    'type': 'note',
                    'description': f'Negative sentiment detected in {negative_notes.count()} notes',
                    'severity': 'medium'
                })

            # Check for concerning keywords
            concern_keywords = ['concern', 'worry', 'issue', 'problem', 'risk', 'danger']
            concerning_notes = recent_notes.filter(
                Q(content__icontains='concern') |
                Q(content__icontains='worry') |
                Q(content__icontains='issue') |
                Q(content__icontains='problem') |
                Q(content__icontains='risk') |
                Q(content__icontains='danger')
            )
            if concerning_notes.count() > 0:
                anomalies.append({
                    'type': 'note',
                    'description': f'Concerning keywords found in {concerning_notes.count()} notes',
                    'severity': 'high'
                })

            return anomalies
        except Exception as e:
            logger.error(f"Error detecting note anomalies: {str(e)}")
            return anomalies

    def _detect_time_of_day_movement(self, child):
        """Detect movement during unusual hours (e.g., 11pm-5am)"""
        anomalies = []
        try:
            recent_locations = Location.objects.filter(
                child=child,
                timestamp__gte=datetime.now() - timedelta(days=7)
            )
            for loc in recent_locations:
                if loc.timestamp.hour >= 23 or loc.timestamp.hour < 5:
                    anomalies.append({
                        'type': 'location',
                        'description': f'Movement detected at unusual hour: {loc.timestamp.strftime("%H:%M")}',
                        'severity': 'medium'
                    })
                    break  # Only flag once per week
            return anomalies
        except Exception as e:
            logger.error(f"Error in time-of-day movement rule: {str(e)}")
            return anomalies

    def _detect_device_tampering(self, child):
        """Detect device tampering (e.g., device removed, reset, or sudden signal loss)"""
        anomalies = []
        try:
            devices = Device.objects.filter(child=child)
            for device in devices:
                # Example: sudden drop in signal strength to zero
                if device.signal_strength == 0:
                    anomalies.append({
                        'type': 'device',
                        'description': f'Device {device.device_token[:10]}... may have been tampered with (signal lost)',
                        'severity': 'high'
                    })
                # Example: device reset (implement your own logic based on your model fields)
                if hasattr(device, 'was_reset') and device.was_reset:
                    anomalies.append({
                        'type': 'device',
                        'description': f'Device {device.device_token[:10]}... was reset',
                        'severity': 'medium'
                    })
            return anomalies
        except Exception as e:
            logger.error(f"Error in device tampering rule: {str(e)}")
            return anomalies

    def _detect_repeated_missed_activities(self, child):
        """Detect 3 or more missed activities in a row"""
        anomalies = []
        try:
            recent_activities = Activity.objects.filter(
                child=child,
                timestamp__gte=datetime.now() - timedelta(days=7)
            ).order_by('-timestamp')[:5]
            missed_streak = 0
            for act in recent_activities:
                if act.status == 'missed':
                    missed_streak += 1
                else:
                    break
            if missed_streak >= 3:
                anomalies.append({
                    'type': 'activity',
                    'description': f'{missed_streak} missed activities in a row',
                    'severity': 'high'
                })
            return anomalies
        except Exception as e:
            logger.error(f"Error in repeated missed activities rule: {str(e)}")
            return anomalies

    def train_model(self, training_data):
        """Train the anomaly detection model"""
        try:
            X = np.array([list(sample['features'].values()) for sample in training_data])

            # Scale features
            X_scaled = self.scaler.fit_transform(X)

            # Train model
            self.model.fit(X_scaled)

            # Save model and scaler
            joblib.dump(self.model, settings.ANOMALY_MODEL_PATH)
            joblib.dump(self.scaler, settings.ANOMALY_SCALER_PATH)

            return True
        except Exception as e:
            logger.error(f"Error training anomaly model: {str(e)}")
            return False

    def evaluate_model(self, test_data):
        """Evaluate model performance"""
        try:
            X = np.array([list(sample['features'].values()) for sample in test_data])
            y = np.array([sample['is_anomaly'] for sample in test_data])

            # Scale features
            X_scaled = self.scaler.transform(X)

            # Get predictions
            y_pred = self.model.predict(X_scaled)
            y_pred = np.where(y_pred == -1, 1, 0)  # Convert to binary

            # Calculate metrics
            accuracy = np.mean(y_pred == y)
            precision = np.mean(y_pred[y == 1] == 1)
            recall = np.mean(y[y_pred == 1] == 1)
            f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0

            return {
                'accuracy': accuracy,
                'precision': precision,
                'recall': recall,
                'f1_score': f1
            }
        except Exception as e:
            logger.error(f"Error evaluating anomaly model: {str(e)}")
            return None 