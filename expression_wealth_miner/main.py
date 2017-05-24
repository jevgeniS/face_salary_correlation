from Analyzer import Analyzer
from RealtimeTest import RealtimeTest
from processing.DataRequester import DataRequester

if __name__ == "__main__":
    RealtimeTest().run_test()
    #faces_df = DataRequester().read_faces_from_urls()

    #analyzer = Analyzer()
    #analyzer.generate_features_and_test(analyzer.create_clf())






