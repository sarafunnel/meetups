from src.data_model import TrainAnnouncement
from src.train_delays import business_rules_converter, clean_data
from test.data import traindata


def substitute_call():
    return str(traindata.train_data)


def test_business_layer(monkeypatch):
    monkeypatch.setattr('train_delays.src.train_delays.data_gathering', substitute_call)
    active_trains, _ = business_rules_converter()
    assert active_trains[2].to_string() == TrainAnnouncement(advertised_time_at_location="2020-01-15T06:40:00.000+01:00", advertised_train_ident=42400, canceled=False, estimated_time_at_location="2020-01-15T06:34:00.000+01:00", delay_in_mins=6.0).to_string()
    assert active_trains[50].to_string() == TrainAnnouncement("2020-01-16T16:19:00.000+01:00", 9118).to_string()


def test_data_cleaning():
    val1 = {'AdvertisedTimeAtLocation': '2020-01-16T16:19:00.000+01:00', 'AdvertisedTrainIdent': '9118', 'Canceled': False}
    val2 = {'AdvertisedTimeAtLocation': '2020-01-16T17:12:00.000+01:00', 'AdvertisedTrainIdent': '4375', 'Canceled': True}
    assert_string = "[delay_in_mins: 0.0, adv_time: 2020-01-16T16:19:00.000+01:00,adv_train_id: 9118, canceled: False, est_time_location: None]"
    assert clean_data(val1).to_string() == assert_string
    assert clean_data(val2) is None
