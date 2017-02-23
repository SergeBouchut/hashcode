import pdb


class Data:
    count = {}
    videos = []
    endpoints = []
    requests = []

    def __init__(self):
        with open('input/me_at_the_zoo.in', 'r') as f:
            (
                self.count['videos'],
                self.count['endpoints'],
                self.count['requests'],
                self.count['cache'],
                self.count['cache_sizes']
            ) = f.readline().split(' ')
            for k, v in self.count.items():
                self.count[k] = int(v)

            for video_size in f.readline().split(' '):
                self.videos.append({
                    'size': int(video_size),
                    'requests': {},
                })

            for endpoint in range(int(self.count['endpoints'])):
                distance, cache_number = f.readline().split(' ')
                caches = {}
                for cache in range(int(cache_number)):
                    cache_id, cache_distance = f.readline().split(' ')
                    caches['id'] = cache_distance.replace("\n", "")
                self.endpoints.append({
                    'distance': distance,
                    'caches': caches,
                })

            for request in range(int(self.count['requests'])):
                video_id, endpoint_id, request_nb = f.readline().split(' ')
                self.videos[int(video_id)]['requests'][int(endpoint_id)] = int(request_nb)

    def calc_

    def __str__(self):
        return "count: " + str(self.count) + "\n\nendpoints: " + str(self.endpoints) + "\nrequests: " + str(self.requests)

if __name__ == "__main__":
    d = Data()

    print(d)
