#---------------------------------------------------------------------------------#
# Results for osgeo.gdal.Open.ReadRaster()                                        #
#---------------------------------------------------------------------------------#
# The 2 Most Common Usages Are: (Derived from 4 Examples)                         #
#    osgeo.gdal.Open.ReadRaster(arg1,arg2,arg3,arg4,arg5,arg6,band_list=) [50.0%] #
#    osgeo.gdal.Open.ReadRaster(arg1,arg2,arg3,arg4) [50.0%]                      #
#---------------------------------------------------------------------------------#
# See Examples of Each Usage Below                                                #
#---------------------------------------------------------------------------------#
# Thoughts? 😞 😐 😀                                                               #
# Please Take our Survey! https://aka.ms/UsageExamplesSurveyC                     #
#---------------------------------------------------------------------------------#
# type: ignore                                                                    #



# Examples for osgeo.gdal.Open.ReadRaster(arg1,arg2,arg3,arg4,arg5,arg6,band_list=) [50.0%]

# Example 1 of 2
# GitHub Source https://github.com/OpenDroneMap/ODM/blob/d5a472eeec0e01e05c949c00ce0b78362899a2c7/opendm/tiles/gdal2tiles.py#L974#L975

def create_base_tile(tile_job_info, tile_detail, queue=None):
    gdal.AllRegister()

    dataBandsCount = tile_job_info.nb_data_bands
    output = tile_job_info.output_file_path
    tileext = tile_job_info.tile_extension
    tilesize = tile_job_info.tile_size
    options = tile_job_info.options

    tilebands = dataBandsCount + 1
    ds = gdal.Open(tile_job_info.src_file, gdal.GA_ReadOnly)
    mem_drv = gdal.GetDriverByName('MEM')
    out_drv = gdal.GetDriverByName(tile_job_info.tile_driver)
    alphaband = ds.GetRasterBand(1).GetMaskBand()

    tx = tile_detail.tx
    ty = tile_detail.ty
    tz = tile_detail.tz
    rx = tile_detail.rx
    ry = tile_detail.ry
    rxsize = tile_detail.rxsize
    rysize = tile_detail.rysize
    wx = tile_detail.wx
    wy = tile_detail.wy
    wxsize = tile_detail.wxsize
    wysize = tile_detail.wysize
    querysize = tile_detail.querysize

    # Tile dataset in memory
    tilefilename = os.path.join(
        output, str(tz), str(tx), "%s.%s" % (ty, tileext))
    dstile = mem_drv.Create('', tilesize, tilesize, tilebands)

    data = alpha = None

    if options.verbose:
        print("\tReadRaster Extent: ",
              (rx, ry, rxsize, rysize), (wx, wy, wxsize, wysize))

    # Query is in 'nearest neighbour' but can be bigger in then the tilesize
    # We scale down the query to the tilesize by supplied algorithm.

    if rxsize != 0 and rysize != 0 and wxsize != 0 and wysize != 0:
        data = ds.ReadRaster(rx, ry, rxsize, rysize, wxsize, wysize,
                             band_list=list(range(1, dataBandsCount+1)))
        alpha = alphaband.ReadRaster(rx, ry, rxsize, rysize, wxsize, wysize)

    # The tile in memory is a transparent file by default. Write pixel values into it if
    # any
    if data:
        if tilesize == querysize:
            # Use the ReadRaster result directly in tiles ('nearest neighbour' query)
            dstile.WriteRaster(wx, wy, wxsize, wysize, data,
                               band_list=list(range(1, dataBandsCount+1)))
            dstile.WriteRaster(wx, wy, wxsize, wysize, alpha, band_list=[tilebands])

            # Note: For source drivers based on WaveLet compression (JPEG2000, ECW,
            # MrSID) the ReadRaster function returns high-quality raster (not ugly
            # nearest neighbour)
            # TODO: Use directly 'near' for WaveLet files
        else:
            # Big ReadRaster query in memory scaled to the tilesize - all but 'near'
            # algo
            dsquery = mem_drv.Create('', querysize, querysize, tilebands)
            # TODO: fill the null value in case a tile without alpha is produced (now
            # only png tiles are supported)
            dsquery.WriteRaster(wx, wy, wxsize, wysize, data,
                                band_list=list(range(1, dataBandsCount+1)))
            dsquery.WriteRaster(wx, wy, wxsize, wysize, alpha, band_list=[tilebands])

            scale_query_to_tile(dsquery, dstile, tile_job_info.tile_driver, options,
                                tilefilename=tilefilename)
            del dsquery

    # Force freeing the memory to make sure the C++ destructor is called and the memory as well as
    # the file locks are released
    del ds
    del data

    if options.resampling != 'antialias':
        # Write a copy of tile to png/jpg
        out_drv.CreateCopy(tilefilename, dstile, strict=0)

    del dstile

    # Create a KML file for this tile.
    if tile_job_info.kml:
        kmlfilename = os.path.join(output, str(tz), str(tx), '%d.kml' % ty)
        if not options.resume or not os.path.exists(kmlfilename):
            with open(kmlfilename, 'wb') as f:
                f.write(generate_kml(
                    tx, ty, tz, tile_job_info.tile_extension, tile_job_info.tile_size,
                    tile_job_info.tile_swne, tile_job_info.options
                ).encode('utf-8'))

    if queue:
        queue.put("tile %s %s %s" % (tx, ty, tz))

# Example 2 of 2
# GitHub Source https://github.com/granularag/pyspatial/blob/8c6d53eeeabf1eedd222db95812453f83a6685bb/scripts/gdal2tiles.py#L1292#L1292

def generate_base_tiles(self):
        """Generation of the base tiles (the lowest in the pyramid) directly from the input raster"""

        if not self.options.quiet:
            print("Generating Base Tiles:")

        if self.options.verbose:
            #mx, my = self.out_gt[0], self.out_gt[3] # OriginX, OriginY
            #px, py = self.mercator.MetersToPixels( mx, my, self.tmaxz)
            #print "Pixel coordinates:", px, py, (mx, my)
            print('')
            print("Tiles generated from the max zoom level:")
            print("----------------------------------------")
            print('')


        # Set the bounds
        tminx, tminy, tmaxx, tmaxy = self.tminmax[self.tmaxz]

        # Just the center tile
        #tminx = tminx+ (tmaxx - tminx)/2
        #tminy = tminy+ (tmaxy - tminy)/2
        #tmaxx = tminx
        #tmaxy = tminy

        ds = self.out_ds
        tilebands = self.dataBandsCount + 1
        querysize = self.querysize

        if self.options.verbose:
            print("dataBandsCount: ", self.dataBandsCount)
            print("tilebands: ", tilebands)

        #print tminx, tminy, tmaxx, tmaxy
        tcount = (1+abs(tmaxx-tminx)) * (1+abs(tmaxy-tminy))
        #print tcount
        ti = 0

        tz = self.tmaxz
        for ty in range(tmaxy, tminy-1, -1): #range(tminy, tmaxy+1):
            for tx in range(tminx, tmaxx+1):

                if self.stopped:
                    break
                ti += 1
                tilefilename = os.path.join(self.output, str(tz), str(tx), "%s.%s" % (ty, self.tileext))
                if self.options.verbose:
                    print(ti,'/',tcount, tilefilename) #, "( TileMapService: z / x / y )"

                if self.options.resume and os.path.exists(tilefilename):
                    if self.options.verbose:
                        print("Tile generation skipped because of --resume")
                    else:
                        self.progressbar( ti / float(tcount) )
                    continue

                # Create directories for the tile
                if not os.path.exists(os.path.dirname(tilefilename)):
                    os.makedirs(os.path.dirname(tilefilename))

                if self.options.profile == 'mercator':
                    # Tile bounds in EPSG:3857
                    b = self.mercator.TileBounds(tx, ty, tz)
                elif self.options.profile == 'geodetic':
                    b = self.geodetic.TileBounds(tx, ty, tz)

                #print "\tgdalwarp -ts 256 256 -te %s %s %s %s %s %s_%s_%s.tif" % ( b[0], b[1], b[2], b[3], "tiles.vrt", tz, tx, ty)

                # Don't scale up by nearest neighbour, better change the querysize
                # to the native resolution (and return smaller query tile) for scaling

                if self.options.profile in ('mercator','geodetic'):
                    rb, wb = self.geo_query( ds, b[0], b[3], b[2], b[1])
                    nativesize = wb[0]+wb[2] # Pixel size in the raster covering query geo extent
                    if self.options.verbose:
                        print("\tNative Extent (querysize",nativesize,"): ", rb, wb)

                    # Tile bounds in raster coordinates for ReadRaster query
                    rb, wb = self.geo_query( ds, b[0], b[3], b[2], b[1], querysize=querysize)

                    rx, ry, rxsize, rysize = rb
                    wx, wy, wxsize, wysize = wb

                else: # 'raster' profile:

                    tsize = int(self.tsize[tz]) # tilesize in raster coordinates for actual zoom
                    xsize = self.out_ds.RasterXSize # size of the raster in pixels
                    ysize = self.out_ds.RasterYSize
                    if tz >= self.nativezoom:
                        querysize = self.tilesize # int(2**(self.nativezoom-tz) * self.tilesize)

                    rx = (tx) * tsize
                    rxsize = 0
                    if tx == tmaxx:
                        rxsize = xsize % tsize
                    if rxsize == 0:
                        rxsize = tsize

                    rysize = 0
                    if ty == tmaxy:
                        rysize = ysize % tsize
                    if rysize == 0:
                        rysize = tsize
                    ry = ysize - (ty * tsize) - rysize

                    wx, wy = 0, 0
                    wxsize, wysize = int(rxsize/float(tsize) * self.tilesize), int(rysize/float(tsize) * self.tilesize)
                    if wysize != self.tilesize:
                        wy = self.tilesize - wysize

                if self.options.verbose:
                    print("\tReadRaster Extent: ", (rx, ry, rxsize, rysize), (wx, wy, wxsize, wysize))

                # Query is in 'nearest neighbour' but can be bigger in then the tilesize
                # We scale down the query to the tilesize by supplied algorithm.

                # Tile dataset in memory
                dstile = self.mem_drv.Create('', self.tilesize, self.tilesize, tilebands)
                data = ds.ReadRaster(rx, ry, rxsize, rysize, wxsize, wysize, band_list=list(range(1,self.dataBandsCount+1)))
                alpha = self.alphaband.ReadRaster(rx, ry, rxsize, rysize, wxsize, wysize)

                if self.tilesize == querysize:
                    # Use the ReadRaster result directly in tiles ('nearest neighbour' query)
                    dstile.WriteRaster(wx, wy, wxsize, wysize, data, band_list=list(range(1,self.dataBandsCount+1)))
                    dstile.WriteRaster(wx, wy, wxsize, wysize, alpha, band_list=[tilebands])

                    # Note: For source drivers based on WaveLet compression (JPEG2000, ECW, MrSID)
                    # the ReadRaster function returns high-quality raster (not ugly nearest neighbour)
                    # TODO: Use directly 'near' for WaveLet files
                else:
                    # Big ReadRaster query in memory scaled to the tilesize - all but 'near' algo
                    dsquery = self.mem_drv.Create('', querysize, querysize, tilebands)
                    # TODO: fill the null value in case a tile without alpha is produced (now only png tiles are supported)
                    #for i in range(1, tilebands+1):
                    #   dsquery.GetRasterBand(1).Fill(tilenodata)
                    dsquery.WriteRaster(wx, wy, wxsize, wysize, data, band_list=list(range(1,self.dataBandsCount+1)))
                    dsquery.WriteRaster(wx, wy, wxsize, wysize, alpha, band_list=[tilebands])

                    self.scale_query_to_tile(dsquery, dstile, tilefilename)
                    del dsquery

                del data

                if self.options.resampling != 'antialias':
                    # Write a copy of tile to png/jpg
                    self.out_drv.CreateCopy(tilefilename, dstile, strict=0)

                del dstile

                # Create a KML file for this tile.
                if self.kml:
                    kmlfilename = os.path.join(self.output, str(tz), str(tx), '%d.kml' % ty)
                    if not self.options.resume or not os.path.exists(kmlfilename):
                        f = open( kmlfilename, 'w')
                        f.write( self.generate_kml( tx, ty, tz ))
                        f.close()

                if not self.options.verbose and not self.options.quiet:
                    self.progressbar( ti / float(tcount) )

# Examples for osgeo.gdal.Open.ReadRaster(arg1,arg2,arg3,arg4) [50.0%]

# Example 1 of 2
# GitHub Source https://github.com/granularag/pyspatial/blob/8c6d53eeeabf1eedd222db95812453f83a6685bb/scripts/gdal2tiles.py#L1407#L1407

def generate_overview_tiles(self):
        """Generation of the overview tiles (higher in the pyramid) based on existing tiles"""

        if not self.options.quiet:
            print("Generating Overview Tiles:")

        tilebands = self.dataBandsCount + 1

        # Usage of existing tiles: from 4 underlying tiles generate one as overview.

        tcount = 0
        for tz in range(self.tmaxz-1, self.tminz-1, -1):
            tminx, tminy, tmaxx, tmaxy = self.tminmax[tz]
            tcount += (1+abs(tmaxx-tminx)) * (1+abs(tmaxy-tminy))

        ti = 0

        # querysize = tilesize * 2

        for tz in range(self.tmaxz-1, self.tminz-1, -1):
            tminx, tminy, tmaxx, tmaxy = self.tminmax[tz]
            for ty in range(tmaxy, tminy-1, -1): #range(tminy, tmaxy+1):
                for tx in range(tminx, tmaxx+1):

                    if self.stopped:
                        break

                    ti += 1
                    tilefilename = os.path.join( self.output, str(tz), str(tx), "%s.%s" % (ty, self.tileext) )

                    if self.options.verbose:
                        print(ti,'/',tcount, tilefilename) #, "( TileMapService: z / x / y )"

                    if self.options.resume and os.path.exists(tilefilename):
                        if self.options.verbose:
                            print("Tile generation skipped because of --resume")
                        else:
                            self.progressbar( ti / float(tcount) )
                        continue

                    # Create directories for the tile
                    if not os.path.exists(os.path.dirname(tilefilename)):
                        os.makedirs(os.path.dirname(tilefilename))

                    dsquery = self.mem_drv.Create('', 2*self.tilesize, 2*self.tilesize, tilebands)
                    # TODO: fill the null value
                    #for i in range(1, tilebands+1):
                    #   dsquery.GetRasterBand(1).Fill(tilenodata)
                    dstile = self.mem_drv.Create('', self.tilesize, self.tilesize, tilebands)

                    # TODO: Implement more clever walking on the tiles with cache functionality
                    # probably walk should start with reading of four tiles from top left corner
                    # Hilbert curve

                    children = []
                    # Read the tiles and write them to query window
                    for y in range(2*ty,2*ty+2):
                        for x in range(2*tx,2*tx+2):
                            minx, miny, maxx, maxy = self.tminmax[tz+1]
                            if x >= minx and x <= maxx and y >= miny and y <= maxy:
                                dsquerytile = gdal.Open( os.path.join( self.output, str(tz+1), str(x), "%s.%s" % (y, self.tileext)), gdal.GA_ReadOnly)
                                if (ty==0 and y==1) or (ty!=0 and (y % (2*ty)) != 0):
                                    tileposy = 0
                                else:
                                    tileposy = self.tilesize
                                if tx:
                                    tileposx = x % (2*tx) * self.tilesize
                                elif tx==0 and x==1:
                                    tileposx = self.tilesize
                                else:
                                    tileposx = 0
                                dsquery.WriteRaster( tileposx, tileposy, self.tilesize, self.tilesize,
                                    dsquerytile.ReadRaster(0,0,self.tilesize,self.tilesize),
                                    band_list=list(range(1,tilebands+1)))
                                children.append( [x, y, tz+1] )

                    self.scale_query_to_tile(dsquery, dstile, tilefilename)
                    # Write a copy of tile to png/jpg
                    if self.options.resampling != 'antialias':
                        # Write a copy of tile to png/jpg
                        self.out_drv.CreateCopy(tilefilename, dstile, strict=0)

                    if self.options.verbose:
                        print("\tbuild from zoom", tz+1," tiles:", (2*tx, 2*ty), (2*tx+1, 2*ty),(2*tx, 2*ty+1), (2*tx+1, 2*ty+1))

                    # Create a KML file for this tile.
                    if self.kml:
                        f = open( os.path.join(self.output, '%d/%d/%d.kml' % (tz, tx, ty)), 'w')
                        f.write( self.generate_kml( tx, ty, tz, children ) )
                        f.close()

                    if not self.options.verbose and not self.options.quiet:
                        self.progressbar( ti / float(tcount) )

# Example 2 of 2
# GitHub Source https://github.com/OpenDroneMap/ODM/blob/d5a472eeec0e01e05c949c00ce0b78362899a2c7/opendm/tiles/gdal2tiles.py#L1114#L1116

def create_overview_tiles(tile_job_info, output_folder, options):
    """Generation of the overview tiles (higher in the pyramid) based on existing tiles"""
    mem_driver = gdal.GetDriverByName('MEM')
    tile_driver = tile_job_info.tile_driver
    out_driver = gdal.GetDriverByName(tile_driver)

    tilebands = tile_job_info.nb_data_bands + 1

    # Usage of existing tiles: from 4 underlying tiles generate one as overview.

    tcount = 0
    for tz in range(tile_job_info.tmaxz - 1, tile_job_info.tminz - 1, -1):
        tminx, tminy, tmaxx, tmaxy = tile_job_info.tminmax[tz]
        tcount += (1 + abs(tmaxx-tminx)) * (1 + abs(tmaxy-tminy))

    ti = 0

    if tcount == 0:
        return

    if not options.quiet:
        print("Generating Overview Tiles:")

    progress_bar = ProgressBar(tcount)
    progress_bar.start()

    for tz in range(tile_job_info.tmaxz - 1, tile_job_info.tminz - 1, -1):
        tminx, tminy, tmaxx, tmaxy = tile_job_info.tminmax[tz]
        for ty in range(tmaxy, tminy - 1, -1):
            for tx in range(tminx, tmaxx + 1):

                ti += 1
                tilefilename = os.path.join(output_folder,
                                            str(tz),
                                            str(tx),
                                            "%s.%s" % (ty, tile_job_info.tile_extension))

                if options.verbose:
                    print(ti, '/', tcount, tilefilename)

                if options.resume and os.path.exists(tilefilename):
                    if options.verbose:
                        print("Tile generation skipped because of --resume")
                    else:
                        progress_bar.log_progress()
                    continue

                # Create directories for the tile
                if not os.path.exists(os.path.dirname(tilefilename)):
                    os.makedirs(os.path.dirname(tilefilename))

                dsquery = mem_driver.Create('', 2 * tile_job_info.tile_size,
                                            2 * tile_job_info.tile_size, tilebands)
                # TODO: fill the null value
                dstile = mem_driver.Create('', tile_job_info.tile_size, tile_job_info.tile_size,
                                           tilebands)

                # TODO: Implement more clever walking on the tiles with cache functionality
                # probably walk should start with reading of four tiles from top left corner
                # Hilbert curve

                children = []
                # Read the tiles and write them to query window
                for y in range(2 * ty, 2 * ty + 2):
                    for x in range(2 * tx, 2 * tx + 2):
                        minx, miny, maxx, maxy = tile_job_info.tminmax[tz + 1]
                        if x >= minx and x <= maxx and y >= miny and y <= maxy:
                            dsquerytile = gdal.Open(
                                os.path.join(output_folder, str(tz + 1), str(x),
                                             "%s.%s" % (y, tile_job_info.tile_extension)),
                                gdal.GA_ReadOnly)
                            if (ty == 0 and y == 1) or (ty != 0 and (y % (2 * ty)) != 0):
                                tileposy = 0
                            else:
                                tileposy = tile_job_info.tile_size
                            if tx:
                                tileposx = x % (2 * tx) * tile_job_info.tile_size
                            elif tx == 0 and x == 1:
                                tileposx = tile_job_info.tile_size
                            else:
                                tileposx = 0
                            dsquery.WriteRaster(
                                tileposx, tileposy, tile_job_info.tile_size,
                                tile_job_info.tile_size,
                                dsquerytile.ReadRaster(0, 0,
                                                       tile_job_info.tile_size,
                                                       tile_job_info.tile_size),
                                band_list=list(range(1, tilebands + 1)))
                            children.append([x, y, tz + 1])

                scale_query_to_tile(dsquery, dstile, tile_driver, options,
                                    tilefilename=tilefilename)
                # Write a copy of tile to png/jpg
                if options.resampling != 'antialias':
                    # Write a copy of tile to png/jpg
                    out_driver.CreateCopy(tilefilename, dstile, strict=0)

                if options.verbose:
                    print("\tbuild from zoom", tz + 1,
                          " tiles:", (2 * tx, 2 * ty), (2 * tx + 1, 2 * ty),
                          (2 * tx, 2 * ty + 1), (2 * tx + 1, 2 * ty + 1))

                # Create a KML file for this tile.
                if tile_job_info.kml:
                    with open(os.path.join(
                        output_folder,
                        '%d/%d/%d.kml' % (tz, tx, ty)
                    ), 'wb') as f:
                        f.write(generate_kml(
                            tx, ty, tz, tile_job_info.tile_extension, tile_job_info.tile_size,
                            get_tile_swne(tile_job_info, options), options, children
                        ).encode('utf-8'))

                if not options.verbose and not options.quiet:
                    progress_bar.log_progress()

