from src.data_model import TrainAnnouncement
from src.train_delays import business_rules_converter, clean_data, runner
from test.data import traindata


def substitute_call():
    return str(traindata.train_data)


def test_business_layer(monkeypatch):
    monkeypatch.setattr('src.train_delays.data_gathering', substitute_call)
    active_trains, _ = business_rules_converter()
    assert active_trains[
               2].to_string() == "[delay_in_mins: 19.0, adv_time: 2020-01-15T06:09:00.000+01:00,adv_train_id: 9102, canceled: False, est_time_location: 2020-01-15T05:50:00.000+01:00]"
    assert active_trains[
               32].to_string() == "[delay_in_mins: 0.0, adv_time: 2020-01-16T09:53:00.000+01:00,adv_train_id: 4005, canceled: False, est_time_location: 2020-01-16T10:01:00.000+01:00]"


def test_data_cleaning():
    val1 = {'AdvertisedTimeAtLocation': '2020-01-16T16:19:00.000+01:00',
            'AdvertisedTrainIdent': '9118', 'Canceled': False}
    val2 = {'AdvertisedTimeAtLocation': '2020-01-16T17:12:00.000+01:00',
            'AdvertisedTrainIdent': '4375', 'Canceled': True}
    assert_string = "[delay_in_mins: 0.0, adv_time: 2020-01-16T16:19:00.000+01:00,adv_train_id: 9118, canceled: False, est_time_location: None]"
    assert clean_data(val1).to_string() == assert_string
    assert clean_data(val2) is None


def test_graph(monkeypatch):
    monkeypatch.setattr('src.train_delays.data_gathering', substitute_call)
    runner()
    assert True is True
