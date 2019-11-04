from FR24Analyzer import FR24Analyzer
# from FR24Analyzer.fit import fit
import time


# from apscheduler.schedulers.background import BackgroundScheduler
# def gatherResults():
#     sched = BackgroundScheduler(daemon=True)
#     sched.add_job(getLandingToIST, 'interval', minutes=1)
#     sched.start()


if __name__ == "__main__":
    analyzer = FR24Analyzer.FR24Analyzer()
    # fitter = fit.Fit()
    # fitter.splitDataSet()
    while True:
        analyzer.getLandingTimeToAirport()
        time.sleep(2)
