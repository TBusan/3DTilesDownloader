from scripts.get_tileset import download_tileset

lon,lat = 114.17242851577525,22.29458442453952
radius = 80
output_path = 'result_hk3'

# MorvpMOddhPnD8aMWU7JCnqLonY=


download_tileset(lon,
                 lat,
                 radius,
                 api_key = 'AIzaSyC9oWR4UAwTOaGaWqsDbpfpGA8s0qbi8s8',
                 output_path='result',
                 thread_count=30)


