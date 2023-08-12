from datetime import datetime, timedelta, date
from Directions import Directions
from RouteComparison import RouteComparison

if __name__ == "__main__":
    with open("input/starts.txt", encoding="utf-8") as f:
        starts_list = [x.rstrip() for x in f]
    with open("input/intermediary.txt", encoding="utf-8") as f:
        intermediary_list = [x.rstrip() for x in f]
    with open("input/ends.txt", encoding="utf-8") as f:
        ends_list = [x.rstrip() for x in f]

    # set up output file and clear old content
    OUTPUT_FILE = "output/directions.json"
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write("\n")

    # 7 days later 14:00 pm
    test_date = date.today() + timedelta(days=7)
    test_datetime = datetime(
        year=test_date.year,
        month=test_date.month,
        day=test_date.day,
        hour=14,
        minute=0,
        second=0,
    )

    LINE_COUNT = 0
    for start, intermediary, end in zip(starts_list, intermediary_list, ends_list):
        LINE_COUNT = LINE_COUNT + 1

        print(f"{LINE_COUNT}: {start}, {intermediary}, {end}")

        route_original = Directions(
            f"place_id:{start}",
            f"place_id:{end}",
            mode="transit",
            alternatives=False,
            output_file=OUTPUT_FILE,
            departure_time=test_datetime,
        )

        route_original.get_directions_transit()
        # route_original.display_directions_result()

        route_alt_1 = Directions(
            f"place_id:{start}",
            f"place_id:{intermediary}",
            mode="transit",
            alternatives=False,
            output_file=OUTPUT_FILE,
            departure_time=test_datetime,
        )

        route_alt_1.get_directions_transit()
        # print(route_alt_1.departure_time)
        # route_alt_1.display_directions_result()

        route_alt_2 = Directions(
            f"place_id:{intermediary}",
            f"place_id:{end}",
            mode="transit",
            alternatives=True,
            output_file=OUTPUT_FILE,
            departure_time=test_datetime,
            # departure_time=test_datetime + timedelta(seconds=route_alt_1.routes[0].total_duration),
        )

        route_alt_2.get_directions_transit()

        alt_transfers = route_alt_1.routes[0].getTransfersTimes() + route_alt_2.routes[0].getTransfersTimes()

        if (
            route_alt_1.routes[0].getTravelModes()[-1][0] == "Walking"
            and route_alt_2.routes[0].getTravelModes()[0][0] == "Walking"
        ):
            alt_transfers = alt_transfers - 1

        # print(f"orig_transfers = {route_original.routes[0].getTransfersTimes()}, alt_transfers = {alt_transfers}")

        rc = RouteComparison(route_original.routes[0], [route_alt_1.routes[0], route_alt_2.routes[0]])
        rc.compute_lowest_wk_weight()

        # if LINE_COUNT == 10:
        #     route_original.display_directions_result()
        #     route_alt_1.display_directions_result()
        #     route_alt_2.display_directions_result()
        #     break
