class Cache:
    def __init__(self, id, size):
        self.id = id
        self.available_size = size
        self.assigned_videos = []

    def assign_video(self, video):
        if video.size > self.available_size or video.id in self.assigned_videos:
            return False
        self.assigned_videos.append(video.id)
        self.available_size -= video.size
        return True


class Video:
    def __init__(self, id, size):
        self.id = id
        self.size = size


class Endpoint:
    def __init__(self, latency):
        self.datacenter_latency = latency
        self.caches_latency = []

    def add_cache_latency(self, cache, latency):
        self.caches_latency.append({
            'cache': cache,
            'latency': latency
        })

    def sort_caches_by_latency(self):
        self.sorted_caches = [
            item['cache']
            for item
            in sorted(
                self.caches_latency,
                key=lambda item: item['latency'],
            )
        ]


class Request:
    def __init__(self, video, endpoint, count):
        self.video = video
        self.endpoint = endpoint
        self.count = count

    def compute_cost(self):
        self.cost = self.count * self.video.size * self.endpoint.datacenter_latency


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


if __name__ == "__main__":
    for filename in (
        'me_at_the_zoo',
        'trending_today',
        'videos_worth_spreading',
        'kittens',
    ):
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

        # sort request from higher to lower cost
        sorted_requests = sorted(
            requests,
            key=lambda request: request.cost,
            reverse=True,
        )

        # find best cache to assigned to video
        for request in sorted_requests:
            for cache in request.endpoint.sorted_caches:
                if cache.assign_video(request.video):
                    break

        # write output data
        output_writer(filename, caches)
