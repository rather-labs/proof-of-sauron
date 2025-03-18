class TestSetup:
    # Image configuration
    TILE_SIZE = 64
    IMAGE_SIZE = 256
    
    # Expected results
    EXPECTED_GRID_SIZE = IMAGE_SIZE // TILE_SIZE  # 256/64 = 4
    EXPECTED_TILES = EXPECTED_GRID_SIZE * EXPECTED_GRID_SIZE  # 4*4 = 16
    
    # Test positions
    TEST_ROW = 1
    TEST_COL = 1
    TEST_POSITION = (TILE_SIZE, TILE_SIZE, TILE_SIZE*2, TILE_SIZE*2)  # (64,64,128,128)