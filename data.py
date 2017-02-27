from datetime import datetime


class Cache:
    def __init__(self, id, size):
        self.id = id
        self.available_size = size
        self.assigned_videos = []

    def assign_video(self, request, caches):
        video = request.video
        # check video not already in cache
        if video.size > self.available_size or video.id in self.assigned_videos:
            return False
        # check video not already in another cache for the endpoint
        for cache_id in request.endpoint.sorted_caches:
            if video.id in caches[cache_id].assigned_videos:
                return False
        self.assigned_videos.append(video.id)
        self.available_size -= video.size
        return True


class Video:
    def __init__(self, id, size):
        self.id = id
        self.size = size
        self.requests = []


class Endpoint:
    def __init__(self, latency):
        self.datacenter_latency = latency
        self.caches = []

    def add_cache_latency(self, cache, latency):
        self.caches.append({
            'id': cache.id,
            'gain': self.datacenter_latency - latency,
        })

    def sort_caches_by_latency(self):
        self.sorted_caches = [
            item['id'] for item in sorted(
                self.caches,
                key=lambda item: item['gain'],
                reverse=True,
            )
        ]


class Request:
    def __init__(self, video, endpoint, count):
        self.video = video
        self.video.requests.append(self)
        self.endpoint = endpoint
        self.count = count

    def compute_cost(self):
        self.cost = self.count * self.video.size * self.endpoint.datacenter_latency

    def compute_cumulated_cost(self):
        self.cumulated_cost = 0
        # add request cost on same video for other endpoint sharing cache
        for request in self.video.requests:
            if any([
                cache_id in self.endpoint.sorted_caches
                for cache_id in request.endpoint.sorted_caches
            ]):
                self.cumulated_cost += request.cost


def input_reader(filename, caches, videos, endpoints, requests):
    with open('input/%s.in' % filename, 'r') as f:
        # global data
        (
            videos_count,
            endpoints_count,
            requests_count,
            caches_count,
            caches_size,
        ) = map(int, f.readline().split())

        # cache data
        for id in range(caches_count):
            caches.append(Cache(id, caches_size))

        # video data
        for id, size in enumerate(map(int, f.readline().split())):
            videos.append(Video(id, size))

        # endpoint data
        for line in range(endpoints_count):
            datacenter_latency, caches_count = map(int, f.readline().split())
            endpoint = Endpoint(datacenter_latency)
            # endpoint-cache data
            for sub_line in range(caches_count):
                cache_id, cache_latency = map(int, f.readline().split())
                endpoint.add_cache_latency(caches[cache_id], cache_latency)
            # sort cache from lower to higher latency
            endpoint.sort_caches_by_latency()
            endpoints.append(endpoint)

        # request data
        for line in range(requests_count):
            video_id, endpoint_id, requests_count = map(int, f.readline().split())
            requests.append(
                Request(
                    videos[video_id],
                    endpoints[endpoint_id],
                    requests_count,
                )
            )


def output_writer(filename, caches):
    with open('output/%s.out' % filename, 'w') as f:
        f.write('%d\n' % len(caches))
        for cache in caches:
            f.write('%d %s\n' % (
                cache.id,
                ' '.join(map(str, cache.assigned_videos))
            ))


if __name__ == '__main__':
    for filename in (
        'me_at_the_zoo',
        'trending_today',
        'videos_worth_spreading',
        'kittens',
    ):
        print(filename)

        # init data
        caches = []
        videos = []
        endpoints = []
        requests = []

        # read input data
        input_reader(filename, caches, videos, endpoints, requests)

        # compute cost for each request
        for request in requests:
            request.compute_cost()

        # compute cumulated cost for each request
        percent = len(requests) / 100
        for index, request in enumerate(requests):
            if index % percent == 0:
                print(
                    '%s --> %02d%%' % (
                        datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                        index / percent,
                    )
                )
            request.compute_cumulated_cost()

        # sort request from higher to lower cost
        sorted_requests = sorted(
            requests,
            key=lambda request: request.cumulated_cost,
            reverse=True,
        )

        # find best cache to assigned to video
        for request in sorted_requests:
            for cache_id in request.endpoint.sorted_caches:
                if caches[cache_id].assign_video(request, caches):
                    break

        # write output data
        output_writer(filename, caches)
