TK_EXIT = -1
TK_LOGOUT = 0
TK_LOGIN = 1
TK_CRAWL_READY = 2
TK_CRAWLING = 3

QUEUE_SUCCESS = "Success"
QUEUE_ABORT = "Abort"
QUEUE_EXIT = "Exit"

CRAWL_SUCCESS = 0
CRAWL_NETWORK_ERROR = 1
CRAWL_PROBLEM_ERROR = 2

WRITE_SUCCESS = 0
WRITE_FAIL = 1

PROB_LIST_SUCCESS = 0
PROB_LIST_NETWORK_ERROR = -1

NETWORK_RECONNECT_TIME = 5

HELP_MESSAGE = '''KOISTUDY Crawler by gs14080 ("Programmer") v.1.0.4

KOISTUDY Crawler ("Crawler") crawls your accepted KOISTUDY submissions.

DISCLAIMER
* The Programmer does not guarantee that the Crawler is bug-proof.
  The Crawler may glitch under certain circumstances including
  Runtime Error, Crawling Error and File/Directory loss.
  In any case whether it is intended or not,
  the Programmer is ineligible for the bug and its effect,
  as written in the License file.
* The Crawler does not collect private data such as KOISTUDY password.
* The Programmer apologizes for the abundant usage of English instead of Korean.
* For the source code, check out this GitHub repo:
  https://github.com/evenharder/koistudy-crawler

Procedure

1. Login with your KOISTUDY account.
2. Select a directory.
  * Warning : Files or subdirectories within the directory
    will be altered if its name coincides with the generated one.
3. Click 'Crawl'.
4. Wait until it's done.

Options

* Enable leading zeros
* Name files and directories with leading zeros. (e.g. 123 -> 0123)

* Create directories
* Create problem-numbered directory for each files.

* Add metadata on header
* Insert metadata on file as a comment.
* The following options are available;

  * Watermark
  * Add text 'Auto-generated by KOISTUDY Crawler'

  * KOISTUDY id
  * Add 'Coder : <USER_ID>'

  * Problem title
  * Add 'Prob No. <PROB_NUM> : <PROB_TITLE>' (utf-8 supported)
  * <PROB_NUM> obeys KOISTUDY style (leading zeros in hexadecimal),
    regardless of options 'Enable leading zeros' and 'Hexadecimal'.

  * Submission url
  * Add 'Submission url : <PROB_URL>'

  * Metadata is not generated if none of the sub-options are selected.

* Hexadecimal
* Name files and directories in hexadecimal. (e.g. 0031 -> 001F)

Libraries
* requests : http://python-requests.org
* BeautifulSoup4 : https://www.crummy.com/software/BeautifulSoup/bs4/
* html5lib : https://github.com/html5lib/html5lib-python

Happy coding!'''
