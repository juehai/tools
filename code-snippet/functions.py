#!/usr/bin/env python2.7

import json
def json_encode(s):
    return json.dumps(s, separators=(',',':'))

def json_decode(s):
    return json.loads(s)

def md5(s):
    import hashlib
    m = hashlib.md5()
    m.update(s)
    return m.hexdigest()

def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc: # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else: raise

def chunklist(target, num):
    def _chunks(l, n):
        """ Yield successive n-sized chunks from l.
        """
        for i in xrange(0, len(l), n):
            yield l[i:i+n]
    return list(_chunks(target, num))

def sendEmail(smtp, user, passwd, me, send_to,
               subject, content, cc_to=None):
    '''
    @smtp SMTP server ip or domain.formart: "smtp.gmail.com:587"
    @user SMTP login user name.
    @passwd SMTP login password.
    @me display this string at "from" when he received mail.
    @to send to who.
    @subject email subject
    @content email content
    '''
    import email
    import mimetypes
    import smtplib
    from email.MIMEMultipart import MIMEMultipart
    from email.MIMEText import MIMEText
    from email.MIMEImage import MIMEImage
    from email.Header import Header
    from email.utils import COMMASPACE,formatdate

    assert(isinstance(send_to, list))
    smtp_host, smtp_port = smtp.split(":")

    toAll = list()
    msg = MIMEText(content.encode('utf-8'), 'html', 'utf-8')
    msg['Subject'] = Header(subject, 'utf-8')
    msg['From'] = me
    msg['To'] = COMMASPACE.join(send_to)
    msg['Date'] = formatdate(localtime=True)

    [toAll.append(i) for i in send_to]

    if cc_to:
        msg['Cc'] = COMMASPACE.join(cc_to)
        [toAll.append(i) for i in cc_to]

    mailServer = smtplib.SMTP(smtp_host, smtp_port)
    mailServer.ehlo()
    mailServer.starttls()
    mailServer.ehlo()
    mailServer.login(user, passwd)
    mailServer.sendmail(user, toAll, msg.as_string())
    mailServer.close()

def check_sensitive_time():
    """
    SENSITIVE_TIMEZONE = 'Pacific/Auckland'
    SENSITIVE_TIME     = '2300-0700'
    """
    import re
    from pytz import timezone
    from datetime import datetime

    if SENSITIVE_TIMEZONE is None or SENSITIVE_TIME is None:
        return False

    regex = re.compile(r'^(\d?\d:?\d\d)-(\d?\d:?\d\d)$')
    t1, t2 = regex.findall(SENSITIVE_TIME)[0]
    t1 = t1.replace(":", "")
    t2 = t2.replace(":", "")

    tz = timezone(SENSITIVE_TIMEZONE)
    now = datetime.now(tz)
    t3 = '%02i%02i' % (now.hour, now.minute)

    if ( t1 < t2 ):
        if ( ( t1 <= t3 ) and ( t3 <= t2 ) ):
            msg = 'Current time %s matched %s%s during test: %s'
            log.warning(msg % (t3, t1, t2, SENSITIVE_TIME))
            return True

    else:
        if ( ( t3 >= t1 ) or ( t3 <= t2 ) ):
            msg = 'Current time %s matched %s%s during test: %s'
            log.warning(msg % (t3, t1, t2, SENSITIVE_TIME))
            return True
    return False

