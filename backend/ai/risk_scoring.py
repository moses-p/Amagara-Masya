import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
import joblib
import logging
from datetime import datetime, timedelta
from django.conf import settings
from django.db.models import Avg, Count, Q
from ..models import Child, RiskScore, Activity, Location, Device, Note

logger = logging.getLogger(__name__)

class RiskScoringSystem:
    def __init__(self):
        self.model = None
        self.scaler = None
        self.load_model()

    def load_model(self):
        """Load the trained model and scaler"""
        try:
            self.model = joblib.load(settings.ML_MODEL_PATH)
            self.scaler = joblib.load(settings.ML_SCALER_PATH)
        except Exception as e:
            logger.error(f"Error loading model: {str(e)}")
            self.model = RandomForestClassifier(n_estimators=100, random_state=42)
            self.scaler = StandardScaler()

    def extract_features(self, child):
        """Extract features for risk scoring"""
        try:
            # Basic demographics
            features = {
                'age': child.age,
                'time_in_care': (datetime.now().date() - child.enrollment_date).days,
                'previous_incidents': child.incidents.count(),
            }

            # Location-based features
            recent_locations = Location.objects.filter(
                child=child,
                timestamp__gte=datetime.now() - timedelta(days=7)
            )
            features.update({
                'location_variance': self._calculate_location_variance(recent_locations),
                'unusual_locations': self._count_unusual_locations(recent_locations),
                'location_updates_frequency': self._calculate_update_frequency(recent_locations),
            })

            # Activity-based features
            recent_activities = Activity.objects.filter(
                child=child,
                timestamp__gte=datetime.now() - timedelta(days=7)
            )
            features.update({
                'activity_variance': self._calculate_activity_variance(recent_activities),
                'missed_activities': self._count_missed_activities(recent_activities),
                'activity_completion_rate': self._calculate_completion_rate(recent_activities),
            })

            # Device-based features
            devices = Device.objects.filter(child=child)
            features.update({
                'device_connectivity': self._calculate_device_connectivity(devices),
                'battery_issues': self._count_battery_issues(devices),
                'signal_strength': self._calculate_signal_strength(devices),
            })

            # Note-based features
            recent_notes = Note.objects.filter(
                child=child,
                created_at__gte=datetime.now() - timedelta(days=30)
            )
            features.update({
                'sentiment_score': self._calculate_sentiment_score(recent_notes),
                'note_frequency': recent_notes.count() / 30,  # notes per day
                'concern_keywords': self._count_concern_keywords(recent_notes),
            })

            return features
        except Exception as e:
            logger.error(f"Error extracting features for child {child.id}: {str(e)}")
            return None

    def calculate_risk_score(self, child):
        """Calculate risk score for a child"""
        try:
            features = self.extract_features(child)
            if not features:
                return None

            # Convert features to array and scale
            feature_array = np.array([list(features.values())])
            scaled_features = self.scaler.transform(feature_array)

            # Get model prediction
            risk_probability = self.model.predict_proba(scaled_features)[0][1]
            risk_score = int(risk_probability * 100)

            # Save risk score
            RiskScore.objects.create(
                child=child,
                score=risk_score,
                factors=self._get_risk_factors(features),
                timestamp=datetime.now()
            )

            return risk_score
        except Exception as e:
            logger.error(f"Error calculating risk score for child {child.id}: {str(e)}")
            return None

    def _calculate_location_variance(self, locations):
        """Calculate variance in location patterns"""
        if not locations:
            return 0
        coordinates = [(loc.latitude, loc.longitude) for loc in locations]
        return np.var(coordinates)

    def _count_unusual_locations(self, locations):
        """Count locations outside normal boundaries"""
        if not locations:
            return 0
        return locations.filter(is_unusual=True).count()

    def _calculate_update_frequency(self, locations):
        """Calculate frequency of location updates"""
        if not locations:
            return 0
        time_span = (locations.last().timestamp - locations.first().timestamp).total_seconds()
        return len(locations) / (time_span / 3600) if time_span > 0 else 0

    def _calculate_activity_variance(self, activities):
        """Calculate variance in activity patterns"""
        if not activities:
            return 0
        completion_times = [act.completion_time for act in activities if act.completion_time]
        return np.var(completion_times) if completion_times else 0

    def _count_missed_activities(self, activities):
        """Count missed or incomplete activities"""
        if not activities:
            return 0
        return activities.filter(status='missed').count()

    def _calculate_completion_rate(self, activities):
        """Calculate activity completion rate"""
        if not activities:
            return 0
        completed = activities.filter(status='completed').count()
        return completed / len(activities)

    def _calculate_device_connectivity(self, devices):
        """Calculate device connectivity score"""
        if not devices:
            return 0
        total_time = 0
        connected_time = 0
        for device in devices:
            if device.last_seen:
                time_since_last_seen = (datetime.now() - device.last_seen).total_seconds()
                if time_since_last_seen < 3600:  # Connected in last hour
                    connected_time += 1
                total_time += 1
        return connected_time / total_time if total_time > 0 else 0

    def _count_battery_issues(self, devices):
        """Count devices with low battery"""
        if not devices:
            return 0
        return devices.filter(battery_level__lt=20).count()

    def _calculate_signal_strength(self, devices):
        """Calculate average signal strength"""
        if not devices:
            return 0
        return devices.aggregate(Avg('signal_strength'))['signal_strength__avg'] or 0

    def _calculate_sentiment_score(self, notes):
        """Calculate sentiment score from notes"""
        if not notes:
            return 0
        # Implement sentiment analysis here
        # This is a placeholder - you should use a proper sentiment analysis model
        return 0.5

    def _count_concern_keywords(self, notes):
        """Count concerning keywords in notes"""
        if not notes:
            return 0
        concern_keywords = ['concern', 'worry', 'issue', 'problem', 'risk', 'danger']
        count = 0
        for note in notes:
            count += sum(1 for keyword in concern_keywords if keyword in note.content.lower())
        return count

    def _get_risk_factors(self, features):
        """Identify key risk factors"""
        risk_factors = []
        if features['location_variance'] > 0.5:
            risk_factors.append('High location variance')
        if features['unusual_locations'] > 0:
            risk_factors.append('Unusual locations detected')
        if features['missed_activities'] > 0:
            risk_factors.append('Missed activities')
        if features['device_connectivity'] < 0.8:
            risk_factors.append('Poor device connectivity')
        if features['battery_issues'] > 0:
            risk_factors.append('Device battery issues')
        if features['sentiment_score'] < 0.3:
            risk_factors.append('Negative sentiment in notes')
        return risk_factors

    def train_model(self, training_data):
        """Train the risk scoring model"""
        try:
            X = np.array([list(sample['features'].values()) for sample in training_data])
            y = np.array([sample['risk_label'] for sample in training_data])

            # Scale features
            X_scaled = self.scaler.fit_transform(X)

            # Train model
            self.model.fit(X_scaled, y)

            # Save model and scaler
            joblib.dump(self.model, settings.ML_MODEL_PATH)
            joblib.dump(self.scaler, settings.ML_SCALER_PATH)

            return True
        except Exception as e:
            logger.error(f"Error training model: {str(e)}")
            return False

    def evaluate_model(self, test_data):
        """Evaluate model performance"""
        try:
            X = np.array([list(sample['features'].values()) for sample in test_data])
            y = np.array([sample['risk_label'] for sample in test_data])

            # Scale features
            X_scaled = self.scaler.transform(X)

            # Get predictions
            y_pred = self.model.predict(X_scaled)
            y_prob = self.model.predict_proba(X_scaled)

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
            logger.error(f"Error evaluating model: {str(e)}")
            return None 