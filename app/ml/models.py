import os
import joblib
import numpy as np

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import LabelEncoder
from xgboost import XGBClassifier


class IntentModel:

    def __init__(self):

        self.model_path = "intent_xgb.pkl"
        self.vectorizer_path = "vectorizer.pkl"
        self.encoder_path = "label_encoder.pkl"

        if os.path.exists(self.model_path):
            self.model = joblib.load(self.model_path)
            self.vectorizer = joblib.load(self.vectorizer_path)
            self.encoder = joblib.load(self.encoder_path)
        else:
            self._initialize_model()
            self._train_initial_model()

    def _initialize_model(self):
        self.vectorizer = TfidfVectorizer(
            max_features=5000,
            ngram_range=(1, 2)
        )

        self.encoder = LabelEncoder()

        self.model = XGBClassifier(
            objective="multi:softprob",
            eval_metric="mlogloss",
            use_label_encoder=False,
            n_estimators=150,
            max_depth=6,
            learning_rate=0.1
        )

    def _train_initial_model(self):
        """
        Initial bootstrap training.
        Replace with real dataset later.
        """

        training_data = [
            "What is AI?",
            "Explain reinforcement learning",
            "Search documentation",
            "Find knowledge about RL",
            "Create new user",
            "Register user",
            "Add log entry",
            "Show logs",
            "List users"
        ]

        labels = [
            "rag",
            "rag",
            "rag",
            "rag",
            "create_user",
            "create_user",
            "create_log",
            "get_logs",
            "get_users"
        ]

        X = self.vectorizer.fit_transform(training_data)

        encoded_labels = self.encoder.fit_transform(labels)

        self.model.fit(X, encoded_labels)

        joblib.dump(self.model, self.model_path)
        joblib.dump(self.vectorizer, self.vectorizer_path)
        joblib.dump(self.encoder, self.encoder_path)

    def predict(self, text: str):

        X = self.vectorizer.transform([text])

        probs = self.model.predict_proba(X)[0]
        prediction_encoded = np.argmax(probs)

        intent = self.encoder.inverse_transform([prediction_encoded])[0]
        confidence = float(np.max(probs))

        return {
            "intent": intent,
            "confidence": confidence
        }