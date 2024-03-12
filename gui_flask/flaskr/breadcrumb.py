
# Store which path the user took to get there. Each path is a corridor. When
# the user opens a collapsed requirement, it goes in another corridor. When
# the user uses a 'go back' link, it removes the last corridor.

class Breadcrumb():
    def __init__(self, prev_arg):
        self.orig_str = None     # Received argument
        self.prev_req_id = None  # Req ID of the last corridor
        self.prev_tree_id = None # Tree ID of the last corridor
        self.prev_str = None     # Breadcrumb without the last corridor
        self.next_str = None     # Breadcrumb prepared with the next corrifor

        if not prev_arg:
            return

        self.orig_str = prev_arg

        # Extract all corridors from the breadcrumb string.
        corridors = prev_arg.split(',')
        assert(len(corridors) > 0,
               "invalid breadcrumb string, expect at least one corridor")

        # Extract requirement ID and tree ID from the last corridor.
        req_id, tree_id = corridors[-1].split(':')
        self.prev_req_id = req_id
        self.prev_tree_id = tree_id

        self.prev_str = ','.join(corridors[0:-1])

    def prepare_next_corridor(self, cur_req_id):
        if self.orig_str:
            self.next_str = '{},{}'.format(self.orig_str, cur_req_id)
        else:
            self.next_str = '{}'.format(cur_req_id)

    def get_next_corridor(self, tree_id):
        return '{}:{}'.format(self.next_str, tree_id)
