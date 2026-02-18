from data_toolkit.duckdb.register_frames.config_normalizer import ConfigNormalizer
from data_toolkit.duckdb.register_frames.factory import FrameFactory
from data_toolkit.duckdb.register_frames.reader import FrameReader
import duckdb

import logging

logging.basicConfig(level=logging.INFO)

def register_frames_from_cfg(cfg, conn: duckdb.DuckDBPyConnection) -> None:
    """
    registers each frame in conn from cfg
    """
    # TODO: assert key matches between cfg_norm, reader, and factory

    cfg_normalizer = ConfigNormalizer()
    reader = FrameReader()
    factory = FrameFactory()

    for cfg_id, raw_src_cfg in cfg.items():

        logging.info(f"processing cfg_id: {cfg_id}")

        clean_cfg = cfg_normalizer.from_cfg(raw_src_cfg)

        frame = factory.make_frame(clean_cfg)

        df = reader.read(frame)

        conn.register(frame.register_as, df)

        logging.info(f"Registered cfg_id: {cfg_id} as {frame.register_as}")





