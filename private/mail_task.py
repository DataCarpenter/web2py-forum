import time

def send_my_mail(to, html_msg):
    print "send mail to: ", to
    print "send msg: ", html_msg
    try:
        mail.send(to, T('You request to keep up to date about your prefered post'), html_msg)
    except Exception, e:
        print ("send mail to: %s failed, retry in 1 min. Error : %s", row.email, e)
    time.sleep(1)

for row in db().select(db.task_interest_mail.email, distinct=True):
    title_array = []
    mail_html_msg = '<html>'
    for task_interest_mail in db(db.task_interest_mail.email==row.email).select():
        try:
            post = db(db.post.id==task_interest_mail.post_id).select().first()
            comment = db(db.comm.id==task_interest_mail.comm_id).select().first()

            if post.title not in title_array:
                title_array.append(post.title)
                mail_html_msg = mail_html_msg + '<hr>'
                mail_html_msg = mail_html_msg + '<h2>' + post.title + '</h2>' + '<br>'

            mail_html_msg = mail_html_msg + T('%s say: ', db.auth_user[comment.created_by].nickname or db.auth_user[comment.created_by].first_name) + T('"%s"', comment.body) + '<br>'

            db(db.task_interest_mail.id==task_interest_mail.id).delete()
            db.commit()
        except Exception, e:
            print ("send mail to: %s failed. Error : %s", task_interest_mail.email, e)

    mail_html_msg = mail_html_msg + '</html>'
    send_my_mail(task_interest_mail.email, mail_html_msg)
