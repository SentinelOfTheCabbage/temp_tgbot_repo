# pylint: disable=C0111,W0401,W0614
import re
import branches
from settings import *
from copy import deepcopy


class main_menu:

    def __init__(self, bot):
        self.branches = branches.get_branches()
        self.bot = bot
        self.current_users = {}
        self.database = DbTeller()
        self.products = self._get_products_list()
        self.admin_list = admin_list
        self.testers_id_list = testers_id_list
        self.dost = Dostavista(self.products)

    def _get_reaction(self, message, callback):
        if message or callback:
            message = Message(message=message, callback=callback)
        else:
            return 0

        user, status = self.get_user(message)
        return message, user, status

    def get_reaction(self, message=None, callback=None):
        message, user, status = self._get_reaction(message, callback)
        current_branch = self.branches[user.get_branch()]['steps']

        # Only for Iphones =|
        if (user.last_message == message.id):
            return None
        else:
            user.answer_status = False
            user.last_message = message.id

        if status == NEW_STATUS:
            cur_phase_num = user.get_phase()
            current_branch[cur_phase_num].on_call(self, user, message)

        elif status == OLD_STATUS:
            if message.is_backbutton():
                # Reduce user's current phase index
                user.set_phase(user.get_phase() - 1)
                cur_phase_num = user.get_phase()
                current_phase = current_branch[cur_phase_num]

                # Гndo last changes
                user = current_phase.on_undo(self, user, message)
                # user = current_phase.on_undo(self, user, message)
                self.set_user(user)
                current_phase.on_call(self, user, message)

            elif message.is_nan():
                # When message contains nan val's from empty buttons e.t.c.
                return 0

            else:
                cur_phase_num = user.get_phase()
                current_phase = current_branch[cur_phase_num]

                # If message is valid, then...
                if current_phase.check_access(self, user, message):
                    # USER      - user's new mask
                    # DIRECTION - emerge|dive|next|previous
                    # ARG       - step_size on emerge
                    user, action_direction, arg = current_phase.on_return(
                        self, user, message)
                    if arg == None:
                        arg = 1
                    if action_direction == 'EMERGE':
                        user.pop_branch()
                        user.set_phase(user.get_phase() + arg)
                    elif action_direction == 'DIVE':
                        user.push_branch(arg[0], arg[1])
                    elif action_direction == 'NEXT':
                        user.set_phase(user.get_phase() + arg)
                    elif action_direction == 'PREVIOUS':
                        user.set_phase(user.get_phase() - arg)
                    elif action_direction == 'CURRENT':
                        pass

                    self.set_user(user)

                    # After branches updates we should ask anything =|

                    current_branch = self.branches[user.get_branch()]['steps']
                    cur_phase_num = user.get_phase()
                    current_phase = current_branch[cur_phase_num]
                    current_phase.on_call(self, user, message)
                else:
                    # If message is invalid
                    self.error_message(message)

        # It helps to not to send duplicates to Iphones
        user.update_answer_status()

    def get_user(self, message):
        user_id = message.user_id
        return_data = (None, None)

        if user_id in self.current_users:
            user = self.current_users[user_id]
            if user.last_message == message.id:
                print('--NO CHANCE IPHONE USER =)--')
                return user, OLD_STATUS

        if user_id in self.current_users:
            restart_commands = [self.branches[k]['restarts']
                                for k in self.branches]
            for pos, restarts in enumerate(restart_commands):
                for cmd in restarts:
                    # self.find_accessible_branch(..., message.content)
                    if re.findall(cmd, message.content):
                        branch_key = list(self.branches.keys())[pos]
                        kwargs = self.branches[branch_key]['start'](message)
                        # send ~menu~ to this func too?

                        kwargs['branch'] = branch_key
                        kwargs['last_message_content'] = message.content

                        user = User(user_id, message.id, kwargs)
                        user.push_branch(branch_key, kwargs['start_phase'])

                        if getattr(user, 'predef_prod', False) in self.products:
                            user.basket.append(
                                deepcopy(self.products[user.predef_prod]))
                        if '/start bonuses' == message.content:
                            user.phase = 1
                        self.current_users[user_id] = user
                        return user, NEW_STATUS

            return self.current_users[user_id], OLD_STATUS
        else:
            trigger_commands = [self.branches[k]['triggers']
                                for k in self.branches]
            for pos, triggers in enumerate(trigger_commands):
                for cmd in triggers:
                    if re.findall(cmd, message.content):
                        branch_key = list(self.branches.keys())[pos]
                        kwargs = self.branches[branch_key]['start'](message)

                        kwargs['branch'] = branch_key
                        kwargs['last_message_content'] = message.content

                        user = User(user_id, message.id, kwargs)
                        user.push_branch(branch_key, kwargs['start_phase'])

                        if getattr(user, 'predef_prod', False) in self.products:
                            user.basket.append(
                                deepcopy(self.products[user.predef_prod]))
                        if '/start bonuses' == message.content:
                            user.phase = 1
                        self.current_users[user_id] = user
                        return user, NEW_STATUS

        print(f'There is no branch for this message:\n"{message.content}"')

    def update_users(self, user_id, user):
        self.current_users[user_id] = user

    def clear_users(self):
        self.current_users = {}

    def error_message(self, message):
        if message.type == 'message':
            text = 'Воспользуйтесь кнопками меню выше'
            self.bot.reply_to(message.message, text)

    def _get_products_list(self) -> dict:
        return self.database.get_products_list()

    def set_user(self, user):
        user_id = user.id
        self.current_users[user_id] = user
