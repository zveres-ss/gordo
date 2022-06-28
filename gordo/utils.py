from collections import OrderedDict
from typing import Optional, List, Dict, cast, Union

from gordo_dataset.metadata import sensor_tags_from_build_metadata
from gordo_dataset.sensor_tag import (
    SensorTag,
    Tag,
    normalize_sensor_tag,
    extract_tag_name,
)

TagsList = List[Union[Dict, List, str, SensorTag]]


def normalize_sensor_tags(
    build_dataset_metadata: dict, tag_list: TagsList, **kwargs: Optional[str]
) -> List[SensorTag]:
    """
    Load tag information from the metadata

    Parameters
    ----------
    build_dataset_metadata: dict
        build_metadata.dataset part of the metadata
    tag_list: TagsList
        Tag list that needs to be loaded
    kwargs: Optional[str]
        Additional fields for `normalize_sensor_tag()`

    Returns
    -------
    List[SensorTag]

    """
    tags: Dict[str, Tag] = OrderedDict()
    for tag in tag_list:
        tag_name: str
        if type(tag) is str:
            tags[cast(str, tag)] = tag
        else:
            normalized_tag = normalize_sensor_tag(tag, **kwargs)
            tag_name = extract_tag_name(normalized_tag)
            tags[tag_name] = normalized_tag
    normalized_sensor_tags = sensor_tags_from_build_metadata(
        build_dataset_metadata, set(tags.keys())
    )
    normalized_tag_list: List[SensorTag] = []
    for tag_name in tags.keys():
        normalized_tag_list.append(normalized_sensor_tags[tag_name])
    return normalized_tag_list
