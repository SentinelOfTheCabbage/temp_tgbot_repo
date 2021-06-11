class Message:

    def __init__(self, message=None, callback=None):
        if (message is None) and not(callback is None):
            self.callback = callback
            self.content = callback.data
            self.id = callback.message.message_id
            self.user_id = callback.from_user.id
            self.type = 'callback'
        elif not(message is None) and (callback is None):
            self.message = message
            self.content = message.text
            self.id = message.message_id
            self.user_id = message.from_user.id
            self.type = 'message'
    def is_restart(self):
        restart_arr = ['restart','/restart','start','/start','заново','старт','рестарт','меню','начало']
        for cmd in restart_arr:
            if cmd in self.content.lower():
                return True
        if self.type == 'callback' and '/start ' in self.content:
            return True
        return False

    def is_backbutton(self):
        if self.type == 'callback' and self.content == 'back':
            return True
        return False

    def is_nan(self):
        if self.type == 'callback' and self.content.lower() in ['none','null','nan','nil']:
            return True
        else:
            return False

    def get_referal(self):
        if '/start ' in self.content:
            if len(self.content) > 7:
                return self.content[8:]
            else:
                return None
        else:
            return None
