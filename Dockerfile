FROM remotepixel/amazonlinux-gdal:2.4.2

ENV PACKAGE_PREFIX=/tmp/python

COPY setup.py setup.py
COPY lambda_tiler_cache/ lambda_tiler_cache/

RUN pip3 install . --no-binary numpy,rasterio -t $PACKAGE_PREFIX -U

ENV PYTHONPATH=$PACKAGE_PREFIX
CMD python3 $PACKAGE_PREFIX/lambda_tiler_cache/scripts/cli.py -l 0.0.0.0
