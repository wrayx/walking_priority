from datetime import datetime, timedelta
from Directions import Directions
from RouteComparison import RouteComparison

if __name__ == "__main__":
    with open("input/starts.txt", encoding="utf-8") as f:
        starts_list = [x.rstrip() for x in f]
    with open("input/intermediary.txt", encoding="utf-8") as f:
        intermediary_list = [x.rstrip() for x in f]
    with open("input/ends.txt", encoding="utf-8") as f:
        ends_list = [x.rstrip() for x in f]

    LINE_COUNT = 0
    for start, intermediary, end in zip(starts_list, intermediary_list, ends_list):
        LINE_COUNT = LINE_COUNT + 1
        print(f"{LINE_COUNT}: {start}, {intermediary}, {end}")

        # wembley park -> convent garden
        route_original = Directions(
            f"place_id:{start}",
            f"place_id:{end}",
            mode="transit",
            alternatives=False,
        )

        route_original.get_directions_transit()
        # route_original.display_directions_result()

        # wembley park -> charing cross

        route_alt_1 = Directions(
            f"place_id:{start}",
            f"place_id:{intermediary}",
            mode="transit",
            alternatives=False,
        )

        route_alt_1.get_directions_transit()
        # print(route_alt_1.departure_time)
        # route_alt_1.display_directions_result()

        # charing cross -> convent garden

        test_datetime = datetime(
            year=2023,
            month=7,
            day=31,
            hour=14,
            minute=0,
            second=0,
        )

        route_alt_2 = Directions(
            f"place_id:{intermediary}",
            f"place_id:{end}",
            mode="walking",
            alternatives=True,
            departure_time=test_datetime + timedelta(seconds=route_alt_1.routes[0].total_duration),
        )

        route_alt_2.get_directions_transit()
        # print(route_alt_2.departure_time)
        # route_alt_1.display_directions_result()

        alt_transfers = route_alt_1.routes[0].getTransfersTimes() + route_alt_2.routes[0].getTransfersTimes()
        # print(f"alt_transfers = {alt_transfers}")

        if (
            route_alt_1.routes[0].getTravelModes()[-1][0] == "Walking"
            and route_alt_2.routes[0].getTravelModes()[0][0] == "Walking"
        ):
            alt_transfers = alt_transfers - 1

        # print(route_original.routes[0].getTravelModes(), "\n")
        # print(route_alt_1.routes[0].getTravelModes())
        # print(route_alt_2.routes[0].getTravelModes())

        print(f"orig_transfers = {route_original.routes[0].getTransfersTimes()}, alt_transfers = {alt_transfers}")

        rc = RouteComparison(route_original.routes[0], [route_alt_1.routes[0], route_alt_2.routes[0]])
        rc.compute_lowest_wk_weight()
        # rc.plot_graph()

        # if LINE_COUNT == 5:
        # break

    # # wembley park -> convent garden

    # route_original = Directions(
    #     "place_id:ChIJN0MeSHwRdkgRHgFzVWFU2ks",
    #     "place_id:ChIJs4GOh8sEdkgRRiBFZKMP8ZE",
    #     mode="transit",
    #     alternatives=False,
    # )

    # route_original.get_directions_transit()
    # route_original.display_directions_result()

    # # wembley park -> charing cross

    # route_alt_1 = Directions(
    #     "place_id:ChIJN0MeSHwRdkgRHgFzVWFU2ks",
    #     "place_id:ChIJra2jTs4EdkgRshPsDJz8OM0",
    #     mode="transit",
    #     alternatives=False,
    # )

    # route_alt_1.get_directions_transit()
    # route_alt_1.display_directions_result()

    # # charing cross -> convent garden

    # route_alt_2 = Directions(
    #     "place_id:ChIJra2jTs4EdkgRshPsDJz8OM0",
    #     "place_id:ChIJs4GOh8sEdkgRRiBFZKMP8ZE",
    #     mode="walking",
    #     alternatives=True,
    # )

    # route_alt_2.get_directions_transit()
    # route_alt_2.display_directions_result()

    # =================

    # # excel london -> bush house

    # route_original = Directions(
    #     "place_id:ChIJ5zC0bnGo2EcR7hZ2UK4c0Co",
    #     "place_id:ChIJ__8_fLUEdkgRXd3d1TaO8nw",
    #     mode="transit",
    #     alternatives=False,
    # )

    # route_original.get_directions_transit()
    # route_original.display_directions_result()

    # # excel london -> tottenham court road

    # route_alt_1 = Directions(
    #     "place_id:ChIJ5zC0bnGo2EcR7hZ2UK4c0Co",
    #     "place_id:ChIJDWnTPy0bdkgRMVxJZfmuDeI",
    #     mode="transit",
    #     alternatives=False,
    # )

    # route_alt_1.get_directions_transit()
    # route_alt_1.display_directions_result()

    # # tottenham court road -> bush house

    # route_alt_2 = Directions(
    #     "place_id:ChIJDWnTPy0bdkgRMVxJZfmuDeI",
    #     "place_id:ChIJ__8_fLUEdkgRXd3d1TaO8nw",
    #     mode="walking",
    #     alternatives=False,
    # )

    # route_alt_2.get_directions_transit()
    # route_alt_2.display_directions_result()

    # =================

    # # paddington -> bush house

    # route_original = Directions(
    #     "place_id:ChIJR3R1t1IFdkgRBBCQVT8sJQo",
    #     "place_id:ChIJ__8_fLUEdkgRXd3d1TaO8nw",
    #     mode="transit",
    #     alternatives=False,
    # )

    # route_original.get_directions_transit()
    # route_original.display_directions_result()

    # # paddington -> bond street

    # route_alt_1 = Directions(
    #     "place_id:ChIJR3R1t1IFdkgRBBCQVT8sJQo",
    #     "place_id:ChIJn8Ps1ywFdkgRJcpkcuK0o0c",
    #     mode="transit",
    #     alternatives=False,
    # )

    # route_alt_1.get_directions_transit()
    # route_alt_1.display_directions_result()

    # # bond street -> bush house

    # route_alt_2 = Directions(
    #     "place_id:ChIJn8Ps1ywFdkgRJcpkcuK0o0c",
    #     "place_id:ChIJ__8_fLUEdkgRXd3d1TaO8nw",
    #     mode="transit",
    #     alternatives=False,
    # )

    # route_alt_2.get_directions_transit()
    # route_alt_2.display_directions_result()

    # rc = RouteComparison(route_original.routes[0], [route_alt_1.routes[0], route_alt_2.routes[0]])
    # rc.compute_lowest_wk_weight()
