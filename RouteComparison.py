import re

from networkx.drawing.nx_agraph import graphviz_layout
import networkx as nx
import googlemaps
import osmnx as ox
import numpy as np
import matplotlib.pyplot as plt
from Route import Route

WK_ROUTE_COLOR = "#81A1C1"
TP_ROUTE_COLOR = "#4C566A"
PLANNING_NODE_COLOR = "#5E81AC"
MID_NODE_COLOR = "#ECEFF4"
NODE_EDGE_COLOR = TP_ROUTE_COLOR
WALK_WEIGHT_UPPER_BOUND = 100
STEP_WEIGHT = 0.01


class RouteComparison:
    def __init__(self, route_original: Route, route_alts: list[Route]) -> None:
        self.route_planning_graph = None
        self.origin = route_original.origin.split(",")[0]
        self.destination = route_original.destination.split(",")[0]

        self.original_route = route_original
        self.alternative_routes = route_alts

        self.original_duration = route_original.total_duration
        self.original_walking_duration = route_original.getTotalWalkingDuration()
        self.original_transport_duration = route_original.getTotalTransportingDuration()
        self.alt_walking_duration = 0
        self.alt_transport_duration = 0

        self.lowest_wk_weight = 1

        self.setup()

    def setup(self):
        """set up the api key for the directions platform"""
        # store api key in api_key variable
        with open("api_key.txt", encoding="utf8") as file:
            self.key = file.readline()

        self.client = googlemaps.Client(self.key)

    def compute_alt_duration(self):
        """compute alternative walking duration"""
        for route in self.alternative_routes:
            self.alt_walking_duration += route.getTotalWalkingDuration()
            self.alt_transport_duration += route.getTotalTransportingDuration()

    def compute_lowest_wk_weight(self):
        """compute lowest walk weight"""
        tmp = 1
        self.compute_alt_duration()
        print(
            f"original_wk_time = {Route.str_duration(self.original_walking_duration)} alt_wk_time = {Route.str_duration(self.alt_walking_duration)}"
        )
        print(
            f"original_tp_time = {Route.str_duration(self.original_transport_duration)} alt_tp_time = {Route.str_duration(self.alt_transport_duration)}"
        )

        while self.shortest_route(wk_weight=tmp) is False and tmp < WALK_WEIGHT_UPPER_BOUND:
            tmp += STEP_WEIGHT

        print(f"wk_weight = {round(tmp, 2)}")

        self.lowest_wk_weight = tmp

        return self.lowest_wk_weight

    def shortest_route(self, wk_weight=1):
        """compute shortest route with different weight assigned"""
        planning_graph = nx.Graph()

        # add original route
        mid_cnt = self.plot_route(planning_graph, self.original_route, 1, wk_weight=wk_weight)

        # add alternative routes
        for route in self.alternative_routes:
            mid_cnt = self.plot_route(planning_graph, route, mid_cnt, wk_weight=wk_weight)

        # calculate shortest path between origin and destination in the weighted graph
        shortest_path = nx.dijkstra_path(planning_graph, self.origin, self.destination, "weight")
        # print(shortest_path)

        for node in shortest_path:
            pattern = re.compile("^mid_")
            # the alternative route is chosen
            if not pattern.match(node) and node != self.origin and node != self.destination:
                return False

        return True

    def plot_graph(self):
        """plot the route comparison graph"""
        self.route_planning_graph = nx.Graph()

        # add original route
        mid_cnt = self.plot_route(self.route_planning_graph, self.original_route, 1)

        # add alternative routes
        for route in self.alternative_routes:
            mid_cnt = self.plot_route(self.route_planning_graph, route, mid_cnt)

        # modify the colour and labels for node
        node_color_map = []
        node_label_map = {}

        for node in self.route_planning_graph.nodes():
            pattern = re.compile("^mid_")
            if not pattern.match(node):
                node_color_map.append(PLANNING_NODE_COLOR)
                node_label_map[node] = node
            else:
                node_color_map.append(MID_NODE_COLOR)
                node_label_map[node] = ""

        # calculate shortest path between origin and destination in the weighted graph
        print(nx.dijkstra_path(self.route_planning_graph, self.origin, self.destination, "weight"))

        edge_weights = nx.get_edge_attributes(self.route_planning_graph, "weight")
        pos = graphviz_layout(self.route_planning_graph, prog="neato")
        pos_label = {k: (v[0], v[1] + 1600) for k, v in pos.items()}
        # pos = nx.get_node_attributes(self.route_planning_graph, "pos")
        # pos_label = {k: (v[0], v[1] + 0.003) for k, v in pos.items()}
        nx.draw_networkx_nodes(
            self.route_planning_graph,
            pos,
            node_size=100,
            node_color=node_color_map,
            linewidths=2,
            edgecolors=NODE_EDGE_COLOR,
        )
        nx.draw_networkx_labels(self.route_planning_graph, pos_label, labels=node_label_map, font_size=10)
        edge_colors = nx.get_edge_attributes(self.route_planning_graph, "color").values()
        edge_styles = list(nx.get_edge_attributes(self.route_planning_graph, "style").values())
        nx.draw_networkx_edges(self.route_planning_graph, pos, edge_color=edge_colors, style=edge_styles, width=3)
        nx.draw_networkx_edge_labels(self.route_planning_graph, pos, edge_weights)
        plt.tight_layout()
        plt.savefig(f"./images/{self.origin} to {self.destination}.png")
        plt.clf()
        # plt.show()

    def plot_route(self, graph, route, cnt, tp_weight=1, wk_weight=1):
        """plot route that are sepatated in walking time and transport time"""
        # get the origin and destination address name
        route_origin = route.origin.split(",")[0]
        route_dest = route.destination.split(",")[0]

        # compute the total walking time and transporting time
        wk_duration = route.getTotalWalkingDuration()
        tp_duration = route.getTotalTransportingDuration()
        # total_duration = route.getTotalDuration()

        wk_weight = wk_duration * wk_weight
        tp_weight = tp_duration * tp_weight

        # origin_loc = self.client.geocode(route.origin)[0]["geometry"]["location"]
        # dest_loc = self.client.geocode(route.destination)[0]["geometry"]["location"]

        # source = (float(origin_loc["lng"]), float(origin_loc["lat"]))
        # target = (float(dest_loc["lng"]), float(dest_loc["lat"]))

        # graph.add_node(route_origin, pos=source)
        # graph.add_node(route_dest, pos=target)
        # print(route_origin, source)

        # plot graph
        if wk_duration == 0:
            graph.add_edge(
                route_origin, route_dest, color=TP_ROUTE_COLOR, style="solid", weight=tp_weight, len=tp_duration
            )
        elif tp_duration == 0:
            graph.add_edge(
                route_origin, route_dest, color=WK_ROUTE_COLOR, style="dashed", weight=wk_weight, len=wk_duration
            )
        else:
            # graph.add_node(
            #     f"mid_{cnt}",
            #     pos=(
            #         (source[0] - target[0]) / total_duration * tp_duration,
            #         (source[1] + target[1]) / 2,
            #     ),
            # )
            # add a intermediate stop for separating wk_duration and tp_duration
            graph.add_edge(
                route_origin, f"mid_{cnt}", color=TP_ROUTE_COLOR, style="solid", weight=tp_weight, len=tp_duration
            )
            graph.add_edge(
                f"mid_{cnt}", route_dest, color=WK_ROUTE_COLOR, style="dashed", weight=wk_weight, len=wk_duration
            )
            cnt += 1

        return cnt
