from unittest import TestCase

# pylint: disable=line-too-long
from common.date import format_datetime_for_file, format_timestamp_for_file, get_utc, timestamp_to_date, iso_to_date, parse_file_name_to_datetime  # noqa: E501


class DateTest(TestCase):

    def test_format_datetime_for_file(self) -> None:
        date = iso_to_date("2019-01-04T16:41:24+00:00")
        result = format_datetime_for_file(date)
        self.assertEqual("2019-01-04T16-41-24p00-00", result)

        date = iso_to_date("2019-01-04T16:41:24-01:00")
        result = format_datetime_for_file(date)
        self.assertEqual("2019-01-04T16-41-24m01-00", result)

    def test_format_timestamp_for_file(self) -> None:
        date = iso_to_date("2019-01-04T16:41:24+00:00")
        result = format_timestamp_for_file(date.timestamp())
        self.assertEqual("2019-01-04T16-41-24p00-00", result)

    def test_get_utc(self) -> None:
        result = get_utc()
        self.assertIsNotNone(result)  # only test that make sense in this world

    def test_timestamp_to_date(self) -> None:
        date = iso_to_date("2019-01-04T16:41:24+00:00")
        result = timestamp_to_date(date.timestamp())
        self.assertEqual(result, date)

    def test_iso_to_date(self) -> None:
        iso_date1 = "2019-01-04T16:41:24+00:00"
        result = iso_to_date(iso_date1)
        self.assertEqual(result.isoformat(), iso_date1)

        iso_date2 = "2019-01-04T16:41:24.000000+0000"
        result = iso_to_date(iso_date2)
        self.assertEqual(result.isoformat(), iso_date1)

        iso_date3 = "2019-01-04T16:41:24.000000+00:00"
        result = iso_to_date(iso_date3)
        self.assertEqual(result.isoformat(), iso_date1)

    def test_parse_file_name_to_datetime(self) -> None:
        date = get_utc()
        result = parse_file_name_to_datetime(format_datetime_for_file(date))
        self.assertEqual(date.replace(microsecond=0), result)

        self.assertRaises(
            Exception,
            parse_file_name_to_datetime,
            "2020-02-07 11-04-21-00-00"
        )
