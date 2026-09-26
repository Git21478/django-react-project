from storages.backends.s3 import S3Storage

class MediaStorage(S3Storage):
    def url(self, name, parameters=None, expire=None, http_method=None):
        return f"http://localhost/media/{name}"