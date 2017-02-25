import json


class Data:
    """Data"""
    count = {}
    videos = []
    endpoints = []
    requests = []

    def __init__(self, filename):
        self.filename = filename
        with open('input/%s.in' % filename, 'r') as f:
            (
                self.count['videos'],
                self.count['endpoints'],
                self.count['requests'],
                self.count['cache'],
                self.count['cache_size']
            ) = f.readline().split(' ')
            for k, v in self.count.items():
                self.count[k] = int(v)

            for video_size in f.readline().split(' '):
                self.videos.append({
                    'size': int(video_size),
                    'requests': {},
                })

            # self.endpoints = [{
            #     'latency_to_datacenter': 1000,
            #     'caches': {
            #           '0': 100,
            #           '1': 200,
            #        }
            # }]

            for endpoint in range(int(self.count['endpoints'])):
                latency_to_datacenter, cache_count = f.readline().split(' ')
                caches = {}
                for cache in range(int(cache_count)):
                    cache_id, cache_distance = f.readline().split(' ')
                    caches[cache_id] = cache_distance.replace("\n", "")
                self.endpoints.append({
                    'latency_to_datacenter': latency_to_datacenter,
                    'caches': caches,
                })

            for request in range(int(self.count['requests'])):
                video_id, endpoint_id, request_count = f.readline().split(' ')
                self.requests.append({
                    'video_id': video_id,
                    'endpoint_id': endpoint_id,
                    'count': int(request_count),
                })
                self.videos[int(video_id)]['requests'][int(endpoint_id)] = int(request_count)

    def get_video_size(self, video_id):
        return int(self.videos[int(video_id)]['size'])

    def ponderate_cache(self):
        self.caches = []
        for cache_id in range(self.count['cache']):
            self.caches.append({
                'remaining_size': self.count['cache_size'],
                'candidate_videos': {},
                'assigned_videos': {},
            })
        for request in self.requests:
            video_id = int(request['video_id'])
            endpoint_id = int(request['endpoint_id'])
            weight = request['count'] * self.get_video_size(video_id)
            endpoint = self.endpoints[endpoint_id]
            for cache_id, cache_latency in endpoint['caches'].items():
                old_weight = self.caches[int(cache_id)]['candidate_videos'].get(video_id, 0)
                self.caches[int(cache_id)]['candidate_videos'][video_id] = (
                    (old_weight + weight) / int(cache_latency))

    def get_most_requested_video(self, cache_id):
        cache = self.caches[cache_id]
        # print(json.dumps(cache, indent=4))
        max_weight = 0
        most_requested_video_id = 0
        for video_id, weight in cache['candidate_videos'].items():
            if int(weight) > max_weight:
                most_requested_video_id = video_id
                max_weight = int(weight)
        return most_requested_video_id

    def assign_video_to_cache(self, video_id, cache_id):
        video_size = self.get_video_size(video_id)
        cache = self.caches[cache_id]
        if video_size < cache['remaining_size']:
            cache['assigned_videos'][video_id] = video_size
            cache['candidate_videos'].pop(video_id)
            cache['remaining_size'] -= video_size

    def print_counts(self):
        print(self.count)

    def print_caches(self):
        print(json.dumps(self.caches[:1], indent=4))

    def export(self):
        with open('output/%s.out' % self.filename, 'w') as f:
            f.write(str(len(self.caches)) + '\n')
            for cache_id, cache in enumerate(self.caches):
                video_ids = ' '.join(map(str, (cache['assigned_videos'].keys())))
                f.write(str(cache_id) + ' ' + video_ids + '\n')


if __name__ == "__main__":
    for filename in ('me_at_the_zoo', 'trending_today', 'videos_worth_spreading', 'kittens'):
        d = Data(filename)
        d.ponderate_cache()
        for trial in range(min(10, int(d.count['videos'] / 10))):
            for cache_id, cache in enumerate(d.caches):
                video_id = d.get_most_requested_video(cache_id)
                d.assign_video_to_cache(video_id, cache_id)
        d.export()
