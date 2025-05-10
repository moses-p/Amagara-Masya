from django.core.management.base import BaseCommand
from children.models import Child, ChildAIProfile
import random
# Uncomment and use if you have a real model
# import joblib
# model = joblib.load('path/to/your/model.pkl')

class Command(BaseCommand):
    help = 'Update escape risk scores for all children using an AI model.'

    def handle(self, *args, **options):
        for child in Child.objects.all():
            profile, created = ChildAIProfile.objects.get_or_create(child=child)
            # --- AI Model Integration Example ---
            # features = [child.age, child.gender, ...]  # Extract real features
            # risk_score = float(model.predict_proba([features])[0][1])
            # profile.escape_risk_score = risk_score
            # --- Placeholder: Remove when real model is ready ---
            profile.escape_risk_score = random.uniform(0, 1)
            profile.save()
        self.stdout.write(self.style.SUCCESS('Updated risk scores for all children.')) 