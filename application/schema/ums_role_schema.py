from pydantic import BaseModel, Field


class UmsRoleSchema(BaseModel):
    '''
    private Long id;

    @ApiModelProperty(value = "名称")
    private String name;

    @ApiModelProperty(value = "描述")
    private String description;

    @ApiModelProperty(value = "后台用户数量")
    private Integer adminCount;

    @ApiModelProperty(value = "创建时间")
    private Date createTime;

    @ApiModelProperty(value = "启用状态：0->禁用；1->启用")
    private Integer status;

    private Integer sort;
    '''
    name: str = Field(..., description='名称')
    description: str = Field(..., description='描述')
    admin_count: int = Field(..., alias='adminCount', description='后台用户数量')
    status: int = Field(..., description='启用状态：0->禁用；1->启用')
    sort: int = Field(..., description='排序')


class UmsRoleUpdateSchema(BaseModel):
    name: str = Field(None, description='名称')
    description: str = Field(None, description='描述')
    admin_count: int = Field(None, alias='adminCount', description='后台用户数量')
    status: int = Field(None, description='启用状态：0->禁用；1->启用')
    sort: int = Field(None, description='排序')
