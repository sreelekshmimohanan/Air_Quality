from django.db import models
import json

class register(models.Model):
    name=models.CharField(max_length=150)
    email=models.CharField(max_length=150)
    phone=models.CharField(max_length=120)
    password=models.CharField(max_length=120)

class AQIPrediction(models.Model):
    user_id = models.CharField(max_length=150)
    features = models.TextField()  # Store pollutant values as JSON string
    predicted_aqi = models.FloatField()
    prediction_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"AQI Prediction: {self.predicted_aqi} for user {self.user_id}"

    def get_features_dict(self):
        """Return features as dictionary"""
        import json
        return json.loads(self.features)

    def set_features_dict(self, features_dict):
        """Set features from dictionary"""
        import json
        self.features = json.dumps(features_dict)

    class Meta:
        ordering = ['-prediction_date']
