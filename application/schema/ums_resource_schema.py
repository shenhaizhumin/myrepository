from pydantic import BaseModel, Field


class UmsResourceSchema(BaseModel):
    '''
     private Long id;

    @ApiModelProperty(value = "创建时间")
    private Date createTime;

    @ApiModelProperty(value = "资源名称")
    private String name;

    @ApiModelProperty(value = "资源URL")
    private String url;

    @ApiModelProperty(value = "描述")
    private String description;

    @ApiModelProperty(value = "资源分类ID")
    private Long categoryId;
    '''
    name: str = Field(..., description='资源名称')
    url: str = Field(..., description='资源URL')
    description: str = Field(None, description='描述')
    category_id: int = Field(..., alias='categoryId', description='资源分类ID')


class UmsResourceUpdateSchema(BaseModel):
    name: str = Field(None, description='资源名称')
    url: str = Field(None, description='资源URL')
    description: str = Field(None, description='描述')
    category_id: int = Field(None, alias='categoryId', description='资源分类ID')
