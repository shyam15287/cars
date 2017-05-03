import os, sys

sys.path.insert(0, os.path.abspath(".."))

from app.algorithm.cars.info_gain.evaluation import PrecisionRecommenderEvaluator
from app.dataset.data_object import DataObject
from app.algorithm.cars.info_gain.info_gain_recommender import InfoGainRecommender

import argparse

def main():
    data_object = DataObject()
    evaluator = PrecisionRecommenderEvaluator()
    recommender = InfoGainRecommender(data_object)
    result = evaluator.evaluate(recommender, data_object, 25, 1.0, 3.5)
    print result
if __name__ == "__main__": main()