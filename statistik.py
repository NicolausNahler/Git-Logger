import argparse
import logging
from logging.handlers import RotatingFileHandler
import subprocess
import matplotlib.pyplot as plt


def get_git_log():
    """
    Returns a list of dictionaries with the git log.
    :return: a list of dictionaries with the git log
    """
    (git_log, _) = subprocess.Popen('git log --pretty=format:%ad', shell=True, stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE).communicate()
    return str(git_log)[2:-1].split('\\n')


def draw_plot(git_log: list):
    """
    Draws a plot with the number of commits per day.
    :param git_log: a list of dictionaries with the git log
    :return:
    """
    days = {"Mon": 0, "Tue": 1, "Wed": 2, "Thu": 3, "Fri": 4, "Sat": 5, "Sun": 6}

    x_y = []
    for commit in git_log:
        date_data = commit.split()
        time = list(map(int, date_data[3].split(':')))
        x_y.append((days[date_data[0]], time[0] + time[1] / 60 + time[2] / 3600))

    plt.figure(figsize=(7, 7), dpi=80)

    plt.title(f'Number of commits: {len(x_y)}')
    plt.xlabel('Time of day')
    plt.ylabel('Day of the week')
    plt.grid(color="lightgrey")

    for x, y in x_y:
        plt.scatter(y, x, color='blue')

    plt.xticks([0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22],
               ["0", "2", "4", "6", "8", "10", "12", "14", "16", "18", "20", "22"])
    plt.yticks([0, 1, 2, 3, 4, 5, 6], ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"])

    plt.savefig('git_log.png')

    logger.info('Plot saved to git_log.png.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    output_mode = parser.add_mutually_exclusive_group()
    output_mode.add_argument("-v", "--verbose", action='store_true', dest="verbose", help="Verbose Output")
    output_mode.add_argument("-q", "--quiet", action='store_true', dest="quiet", help="Quiet Output")

    args = parser.parse_args()

    logger = logging.getLogger('path_creation')
    logger.setLevel(logging.DEBUG if args.verbose else logging.WARNING)

    rfh = RotatingFileHandler('logging/logging.log', maxBytes=10000, backupCount=5, encoding="utf-8")
    rfh.setLevel(logger.getEffectiveLevel())

    ch = logging.StreamHandler()
    ch.setLevel(logger.getEffectiveLevel())

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    rfh.setFormatter(formatter)
    ch.setFormatter(formatter)

    logger.addHandler(rfh)
    logger.addHandler(ch)

    logger.info("Started script.")

    log = get_git_log()
    draw_plot(log)

    logger.info("Finished script.")
