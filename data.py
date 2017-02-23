import pdb


class Data:

    count = {}
    video_sizes = []
    endpoints = []
    requests = []

    def __init__(self):
        with open('input/me_at_the_zoo.in', 'r') as f:
            pdb.set_trace()

            (
                self.count['videos'],
                self.count['endpoints'],
                self.count['requests'],
                self.count['cache'],
                self.count['cache_sizes']
            ) = f.readline().split(' ')
            for k, v in self.count:
                self.count['k'] = int(v)

            self.video_size = f.readline().split(' ')

            for endpoint in range(self.count['endpoints']):
                distance, cache_number = f.readline().split(' ')
                caches = {}
                for cache in range(int(cache_number)):
                    cache_id, cache_distance = f.readline().split(' ')
                    caches['id'] = cache_distance
                self.endpoints.append({
                    'distance': distance,
                    'caches': caches,
                })

            for request in range(self.count['requests']):
                video_id, endpoint_id, request_nb = f.readline().split(' ')
                self.requests.append({
                    'video': video_id,
                    'endpoint': endpoint_id,
                    'count': request_nb,
                })
