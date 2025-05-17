from rest_framework.throttling import UserRateThrottle, AnonRateThrottle


class BurstRateThrottle(UserRateThrottle):
    scope = 'burst'


class SustainedRateThrottle(UserRateThrottle):
    scope = 'sustained'


class WatchlistRateThrottle(UserRateThrottle):
    scope = 'watchlist'
    rate = '10/minute'  # Limit watchlist operations to 10 per minute


class SearchRateThrottle(UserRateThrottle):
    scope = 'search'
    rate = '20/minute'  # Limit search operations to 20 per minute


class AuthRateThrottle(AnonRateThrottle):
    scope = 'auth'
    rate = '5/minute'  # Limit authentication attempts to 5 per minute
