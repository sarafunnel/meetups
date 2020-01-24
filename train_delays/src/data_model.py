class TrainAnnouncement:
    def __init__(
        self,
        advertised_time_at_location,
        advertised_train_ident,
        canceled=False,
        estimated_time_at_location=None,
        delay_in_mins=0.0,
    ):
        self.delay_in_mins = delay_in_mins
        self.adv_time = advertised_time_at_location
        self.adv_train_id = advertised_train_ident
        self.canceled = canceled
        self.est_time_location = estimated_time_at_location

    def add_delay(self, nr):
        self.delay_in_mins = nr

    def to_string(self):
        return (
            f"[delay_in_mins: {self.delay_in_mins}, adv_time: {self.adv_time},"
            f"adv_train_id: {self.adv_train_id}, canceled: {self.canceled}, est_time_location: {self.est_time_location}]"
        )


class FakeStream:
    def __init__(self, file_object):
        self.file_object = file_object

    def iter_lines(self, *_, **__):
        return self.file_object.readlines()
