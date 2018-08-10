import leancloud
# import logging


# logging.basicConfig(level=logging.DEBUG)
def init_account(APPID, APPKEY):
    leancloud.init(APPID, APPKEY)


Comment = leancloud.Object.extend('Comment')


def build_object(comment_data):
    comment = Comment()
    comment.set('nick', comment_data['name'])
    comment.set('mail', comment_data['email'])
    comment.set('url', comment_data['thread_url'])
    comment.set('comment', comment_data['message'])
    comment.set('status', 1)
    return comment


def save_all(comment_list):
    Comment.save_all(comment_list)
