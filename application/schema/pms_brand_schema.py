from pydantic import BaseModel, Field


class PmsBrandSchema(BaseModel):
    first_letter: str = Field(None, description='首字母', alias='firstLetter')
    name: str = Field(..., description='品牌名称')
    logo: str = Field(..., description='品牌logo')
    big_pic: str = Field(None, description='专区大图', alias='bigPic')
    brand_story: str = Field(None, description='品牌故事', alias='brandStory')
    sort: int = Field(0, description='排序', ge=0)
    show_status: int = Field(..., ge=0, le=1, description='是否进行显示', alias='showStatus')
    # product_count: int = Field(...)
    # product_comment_count = Field(...)
    factory_status: int = Field(..., ge=0, le=1, description='是否为品牌制造商：0->不是；1->是', alias='factoryStatus')


class PmsBrandUpdateSchema(BaseModel):
    first_letter: str = Field(None, description='首字母', alias='firstLetter')
    name: str = Field(None, description='品牌名称')
    logo: str = Field(None, description='品牌logo')
    big_pic: str = Field(None, description='专区大图', alias='bigPic')
    brand_story: str = Field(None, description='品牌故事', alias='brandStory')
    sort: int = Field(0, description='排序', ge=0)
    show_status: int = Field(None, ge=0, le=1, description='是否进行显示', alias='showStatus')
    # product_count: int = Field(None)
    # product_comment_count = Field(None)
    factory_status: int = Field(None, ge=0, le=1, description='是否为品牌制造商：0->不是；1->是', alias='factoryStatus')
