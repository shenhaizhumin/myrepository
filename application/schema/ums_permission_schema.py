from pydantic import BaseModel, Field


class UmsPermissionSchema(BaseModel):
    '''
    @ApiModelProperty(value = "父级权限id")
    private Long pid;

    @ApiModelProperty(value = "名称")
    private String name;

    @ApiModelProperty(value = "权限值")
    private String value;

    @ApiModelProperty(value = "图标")
    private String icon;

    @ApiModelProperty(value = "权限类型：0->目录；1->菜单；2->按钮（接口绑定权限）")
    private Integer type;

    @ApiModelProperty(value = "前端资源路径")
    private String uri;

    @ApiModelProperty(value = "启用状态；0->禁用；1->启用")
    private Integer status;

    @ApiModelProperty(value = "创建时间")
    private Date createTime;

    @ApiModelProperty(value = "排序")
    private Integer sort;
    '''
    pid: int = Field(..., description='父级权限id')
    name: str = Field(..., description='名称')
    value: str = Field(None, description='权限值')
    icon: str = Field(None, description='图标')
    type: int = Field(..., description='权限类型：0->目录；1->菜单；2->按钮（接口绑定权限）')
    uri: str = Field(None, description='前端资源路径')
    status: int = Field(..., description='启用状态；0->禁用；1->启用')
    sort: int = Field(..., description='排序')


class UmsPermissionUpdateSchema(BaseModel):
    pid: int = Field(None, description='父级权限id')
    name: str = Field(None, description='名称')
    value: str = Field(None, description='权限值')
    icon: str = Field(None, description='图标')
    type: int = Field(None, description='权限类型：0->目录；1->菜单；2->按钮（接口绑定权限）')
    uri: str = Field(None, description='前端资源路径')
    status: int = Field(None, description='启用状态；0->禁用；1->启用')
    sort: int = Field(None, description='排序')
