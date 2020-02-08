"""
Every function should return a tuple of 2 things
-   (False, None) = Codeforces dies
-   (False, ...)  = Codeforces returns a FAILED status + a comment
-   (True, ...)   = It works
"""

import requests

"""
List of self-made simple APIs
"""

def get_user_info(handle):
    """
    Returns information about one or several users.
    """

    info = requests.get(f'https://codeforces.com/api/user.info?handles={handle}')

    if info.status_code != 200:
        return (0, None)
    
    info = info.json()

    if info['status'] != 'OK':
        return (0, info['comment'])
    
    return (1, User(**info['result'][0]))

def blogEntry_comments(blogEntryId):
    url = f'https://codeforces.com/api/blogEntry.comments?blogEntryId={blogEntryId}'

    info = requests.get(url)
    if info.status_code != 200:
        return (0, None)
    info = info.json()
    if info['status'] != 'OK':
        return (0, info['comment'])
    
    return True, [Comment(**x) for x in info['result']]

def get_user_submissions(handle):
    """
    Get submissions of an user
    """
    info = requests.get(f'https://codeforces.com/api/user.status?handle={handle}')

    if info.status_code != 200:
        return (0, None)
    info = info.json()
    if info['status'] != 'OK':
        return (0, member_bad(info['comment']))

    print(type(info))
    print(type(info['result']))
    print(type(info['result'][0]))
    return (1, [Submission(**x) for x in info['result']])

def get_user_rating_changes(handle):
    """
    Get rating changes of an user
    """
    info = requests.get(f'https://codeforces.com/api/user.rating?handle={handle}')

    if info.status_code != 200:
        return (0, None)
    if info['status'] != 'OK':
        return (0, member_bad(info['comment']))
    
    return (1, [RatingChange(**x) for x in info['result']])

def get_user_blog_entries(handle):
    """
    Get blog entries of an user
    """
    info = requests.get(f'https://codeforces.com/api/user.blogEntries?handle={handle}')

    if info.status_code != 200:
        return (0, None)
    if info['status'] != 'OK':
        return (0, member_bad(info['comment']))
    
    return (1, [BlogEntry(**x) for x in info['result']])

def get_problems(tags):
    """
    Get problems in problemset. Can use tags (list).
    """

    url = f'https://codeforces.com/api/user.blogEntries?handle={handle}?'
    if len(tags):
        url += 'tags=' + ';'.join(tags)

    info = requests.get(url)

    if info.status_code != 200:
        return (0, None)
    if info['status'] != 'OK':
        return (0, member_bad(info['comment']))
    
    return (1, [Problem(**x) for x in info['result']])

def get_contest_standing(contestId, handles = [], showUnofficial = True):
    """
    Get standing of a contest.
    """
    url = f'https://codeforces.com/api/contest.standings?contestId={contestId}&showUnofficial={showUnofficial}'

    if len(handles) > 0:
        url += '&handles=' + ';'.join(handles)

    info = request(url)
    if info.status_code != 200:
        return (0, None)
    if info['status'] != 'OK':
        return (0, member_bad(info['comment']))
    
    return (1, info['result'])

"""
All given methods
(https://codeforces.com/apiHelp/methods)
"""

"""
Classes to store Codeforces's Object
"""
class CodeforcesObject:
    def dict_init(self, **kwargs):
        self.__dict__.update(**kwargs)
    
class User(CodeforcesObject):
    def __init__(self, **kwargs):
        self.handle                 = None  # String. Codeforces user handle.
        self.email                  = None  # String. Shown only if user allowed to share his contact info.
        self.vkId                   = None  # String. User id for VK social network. Shown only if user allowed to share his contact info.
        self.openId                 = None  # String. Shown only if user allowed to share his contact info.
        self.firstName              = None  # String. Localized. Can be absent.
        self.lastName               = None  # String. Localized. Can be absent.
        self.country                = None  # String. Localized. Can be absent.
        self.city                   = None  # String. Localized. Can be absent.
        self.organization           = None  # String. Localized. Can be absent.
        self.contribution           = None  # Integer. User contribution.
        self.rank                   = 'unrated'  # String. Localized.
        self.rating                 = 'unrated'  # Integer.
        self.maxRank                = None  # String. Localized.
        self.maxRating              = None  # Integer.
        self.lastOnlineTimeSeconds  = None  # Integer. Time, when user was last seen online, in unix format.
        self.registrationTimeSeconds= None  # Integer. Time, when user was registered, in unix format.
        self.friendOfCount          = None  # Integer. Amount of users who have this user in friends.
        self.avatar                 = None  # String. User's avatar URL.    
        self.titlePhoto             = None  # String. User's title photo URL.
        self.dict_init(**kwargs)

class BlogEntry(CodeforcesObject):
    def __init__(self, **kwargs):
        self.id                     = None  # Integer.
        self.originalLocale         = None 	# String. Original locale of the blog entry.
        self.creationTimeSeconds    = None  # Integer. Time, when blog entry was created, in unix format.
        self.authorHandle           = None  # String. Author user handle.
        self.title                  = None  # String. Localized.
        self.content                = None  # String. Localized. Not included in short version.
        self.locale                 = None  # String.
        self.modificationTimeSeconds= None  # Integer. Time, when blog entry has been updated, in unix format.
        self.allowViewHistory       = None  # Boolean. If true, you can view any specific revision of the blog entry.
        self.tags                   = None  # String list.
        self.rating                 = None  # Integer.
        self.dict_init(**kwargs)

class Comment(CodeforcesObject):
    def __init__(self, **kwargs):
        self.id                     = None  # Integer.
        self.creationTimeSeconds    = None 	# Integer. Time, when comment was created, in unix format.
        self.commentatorHandle      = None 	# String.
        self.locale                 = None 	# String.
        self.text                   = None 	# String.
        self.parentCommentId        = None  # Integer. Can be absent.
        self.rating                 = None  # Integer.
        self.dict_init(**kwargs)

class RecentAction(CodeforcesObject):
    def __init__(self, **kwargs):
        self.timeSeconds            = None 	# Integer. Action time, in unix format.
        self.blogEntry              = None 	# BlogEntry object in short form. Can be absent.
        self.comment                = None 	# Comment object. Can be absent.
        self.dict_init(**kwargs)
    
    def dict_init(self, **kwargs):
        self.__dict__.update(**kwargs)

        if 'blogEntry' in kwargs:
            setattr(self, 'blogEntry', BlogEntry(**kwargs))

class RatingChange(CodeforcesObject):
    def __init__(self, **kwargs):
        self.contestId              = None 	# Integer.
        self.contestName            = None 	# String. Localized.
        self.handle                 = None	# String. Codeforces user handle.
        self.rank                   = None	# Integer. Place of the user in the contest. This field contains user rank on the moment of rating update. If afterwards rank changes (e.g. someone get disqualified), this field will not be update and will contain old rank.
        self.ratingUpdateTimeSeconds= None 	# Integer. Time, when rating for the contest was update, in unix-format.
        self.oldRating              = None 	# Integer. User rating before the contest.
        self.newRating              = None	# Integer. User rating after the contest.
        self.dict_init(**kwargs)

class Contest(CodeforcesObject):
    def __init__(self, **kwargs):
        self.id 	                = None  # Integer.
        self.name 	                = None  # String. Localized.
        self.type 	                = None  # Enum: CF, IOI, ICPC. Scoring system used for the contest.
        self.phase 	                = None  # Enum: BEFORE, CODING, PENDING_SYSTEM_TEST, SYSTEM_TEST, FINISHED.
        self.frozen 	            = None  # Boolean. If true, then the ranklist for the contest is frozen and shows only submissions, created before freeze.
        self.durationSeconds 	    = None  # Integer. Duration of the contest in seconds.
        self.startTimeSeconds       = None	# Integer. Can be absent. Contest start time in unix format.
        self.relativeTimeSeconds    = None	# Integer. Can be absent. Number of seconds, passed after the start of the contest. Can be negative.
        self.preparedBy 	        = None  # String. Can be absent. Handle of the user, how created the contest.
        self.websiteUrl 	        = None  # String. Can be absent. URL for contest-related website.
        self.description 	        = None  # String. Localized. Can be absent.
        self.difficulty 	        = None  # Integer. Can be absent. From 1 to 5. Larger number means more difficult problems.
        self.kind 	                = None  # String. Localized. Can be absent. Human-readable type of the contest from the following categories: Official ICPC Contest, Official School Contest, Opencup Contest, School/University/City/Region Championship, Training Camp Contest, Official International Personal Contest, Training Contest.
        self.icpcRegion 	        = None  # String. Localized. Can be absent. Name of the Region for official ICPC contests.
        self.country                = None	# String. Localized. Can be absent.
        self.city                   = None	# String. Localized. Can be absent.
        self.season 	            = None  # String. Can be absent.
        self.dict_init(**kwargs)

class Party(CodeforcesObject):
    def __init__(self, **kwargs):
        self.contestId              = None	# Integer. Can be absent. Id of the contest, in which party is participating.
        self.members 	            = None  # List of Member objects. Members of the party.
        self.participantType 	    = None  # Enum: CONTESTANT, PRACTICE, VIRTUAL, MANAGER, OUT_OF_COMPETITION.
        self.teamId 	            = None  # Integer. Can be absent. If party is a team, then it is a unique team id. Otherwise, this field is absent.
        self.teamName               = None	# String. Localized. Can be absent. If party is a team or ghost, then it is a localized name of the team. Otherwise, it is absent.
        self.ghost                  = None	# Boolean. If true then this party is a ghost. It participated in the contest, but not on Codeforces. For example, Andrew Stankevich Contests in Gym has ghosts of the participants from Petrozavodsk Training Camp.
        self.room                   = None	# Integer. Can be absent. Room of the party. If absent, then the party has no room.
        self.startTimeSeconds       = None	# Integer. Can be absent. Time, when this party started a contest.
        self.dict_init(**kwargs)

    def dict_init(self, **kwargs):
        self.__dict__.update(**kwargs)

        if 'members' in kwargs:
            setattr(self, 'members', [Member(**x) for x in kwargs['members']])

class Member(CodeforcesObject):
    def __init__(self, **kwargs):
        self.handle                 = None  # String. Codeforces user handle.
        self.dict_init(**kwargs)

class Problem(CodeforcesObject):
    def __init__(self, **kwargs):
        self.contestId              = None 	# Integer. Can be absent. Id of the contest, containing the problem.
        self.problemsetName         = None	# String. Can be absent. Short name of the problemset the problem belongs to.
        self.index                  = None	# String. Usually a letter of a letter, followed by a digit, that represent a problem index in a contest.
        self.name                   = None	# String. Localized.
        self.type                   = None	# Enum: PROGRAMMING, QUESTION.
        self.points                 = None	# Floating point number. Can be absent. Maximum ammount of points for the problem.
        self.rating                 = None	# Integer. Can be absent. Problem rating (difficulty).
        self.tags                   = None	# String list. Problem tags.
        self.dict_init(**kwargs)

class ProblemStatistics(CodeforcesObject):
    def __init_(self, **kwargs):
        self.contestId 	            = None  # Integer. Can be absent. Id of the contest, containing the problem.
        self.index              	= None  # String. Usually a letter of a letter, followed by a digit, that represent a problem index in a contest.
        self.solvedCount 	        = None  # Integer. Number of users, who solved the problem.
        self.dict_init(**kwargs)

class Submission(CodeforcesObject):
    def __init__(self, **kwargs):
        self.id                     = None  # Integer.
        self.contestId              = None  # Integer. Can be absent.
        self.creationTimeSeconds    = None  # Integer. Time, when submission was created, in unix-format.
        self.relativeTimeSeconds    = None  # Integer. Number of seconds, passed after the start of the contest (or a virtual start for virtual parties), before the submission.
        self.problem                = None  # Problem object.
        self.author                 = None  # Party object.
        self.programmingLanguage    = None  # String.
        self.verdict                = None  # Enum: FAILED, OK, PARTIAL, COMPILATION_ERROR, RUNTIME_ERROR, WRONG_ANSWER, PRESENTATION_ERROR, TIME_LIMIT_EXCEEDED, MEMORY_LIMIT_EXCEEDED, IDLENESS_LIMIT_EXCEEDED, SECURITY_VIOLATED, CRASHED, INPUT_PREPARATION_CRASHED, CHALLENGED, SKIPPED, TESTING, REJECTED. Can be absent.
        self.testset                = None  # Enum: SAMPLES, PRETESTS, TESTS, CHALLENGES, TESTS1, ..., TESTS10. Testset used for judging the submission.
        self.passedTestCount        = None  # Integer. Number of passed tests.
        self.timeConsumedMillis     = None  # Integer. Maximum time in milliseconds, consumed by solution for one test.
        self.memoryConsumedBytes    = None  # Integer. Maximum memory in bytes, consumed by solution for one test.
        self.dict_init(**kwargs)

    def dict_init(self, **kwargs):
        self.__dict__.update(**kwargs)

        if 'problem' in kwargs:
            setattr(self, 'problem', Problem(**kwargs['problem']))
        
        if 'author' in kwargs:
            setattr(self, 'author', Party(**kwargs['author']))

class Hack(CodeforcesObject):
    def __init__(self, **kwargs):
        self.id                     = None 	# Integer.
        self.creationTimeSeconds    = None	# Integer. Hack creation time in unix format.
        self.hacker                 = None	# Party object.
        self.defender               = None	# Party object.
        self.verdict                = None	# Enum: HACK_SUCCESSFUL, HACK_UNSUCCESSFUL, INVALID_INPUT, GENERATOR_INCOMPILABLE, GENERATOR_CRASHED, IGNORED, TESTING, OTHER. Can be absent.
        self.problem                = None	# Problem object. Hacked problem.
        self.test                   = None	# String. Can be absent.
        self.judgeProtocol          = None	# Object with three fields: "manual", "protocol" and "verdict". Field manual can have values "true" and "false". If manual is "true" then test for the hack was entered manually. Fields "protocol" and "verdict" contain human-readable description of judge protocol and hack verdict. Localized. Can be absent.
        self.dict_init(**kwargs)
    
    def dict_init(self, **kwargs):
        self.__dict__.update(**kwargs)

        if 'hacker' in kwargs:
            setattr(self, 'hacker', Party(**kwargs['hacker']))
        
        if 'defender' in kwargs:
            setattr(self, 'defender', Party(kwargs['defender']))
        
        if 'problem' in kwargs:
            setattr(self, 'problem', Problem(kwargs['problem']))

class RanklistRow(CodeforcesObject):
    def __init__(self, **kwargs):
        self.party                  = None	# Party object. Party that took a corresponding place in the contest.
        self.rank                   = None	# Integer. Party place in the contest.
        self.points                 = None	# Floating point number. Total ammount of points, scored by the party.
        self.penalty                = None	# Integer. Total penalty (in ICPC meaning) of the party.
        self.successfulHackCount    = None	# Integer.
        self.unsuccessfulHackCount  = None	# Integer.
        self.problemResults         = None	# List of ProblemResult objects. Party results for each problem. Order of the problems is the same as in "problems" field of the returned object.
        self.lastSubmissionTimeSeconds=None	# Integer. For IOI contests only. Time in seconds from the start of the contest to the last submission that added some points to the total score of the party.
        self.dict_init(**kwargs)
    
    def dict_init(self, **kwargs):
        self.__dict__.update(**kwargs)

        if 'party' in kwargs:
            setattr(self, 'party', Party(kwargs['party']))
        
        if 'problemResults' in kwargs:
            setattr(self, 'problemResults', [ProblemResult(**x) for x in kwargs['problemResults']])

class ProblemResult(CodeforcesObject):
    def __init__(self, **kwargs):
        self.points                 = None	# Floating point number.
        self.penalty                = None	# Integer. Penalty (in ICPC meaning) of the party for this problem.
        self.rejectedAttemptCount   = None 	# Integer. Number of incorrect submissions.
        self.type                   = None	# Enum: PRELIMINARY, FINAL. If type is PRELIMINARY then points can decrease (if, for example, solution will fail during system test). Otherwise, party can only increase points for this problem by submitting better solutions.
        self.bestSubmissionTimeSeconds=None # Integer. Number of seconds after the start of the contest before the submission, that brought maximal amount of points for this problem.
        self.dict(**kwargs)