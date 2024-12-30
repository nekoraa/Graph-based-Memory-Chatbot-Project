import networkx as nx
import pickle

from 记忆体.记忆图操作函数 import 检查或加载记忆图, 绘制图, 保存图为_json, 遍历边, 遍历节点

记忆图 = 检查或加载记忆图()
import plotly.graph_objects as go


def 显示交互式图(graph):
    # 获取布局
    pos = nx.spring_layout(graph)  # 计算图的布局

    # 提取边的坐标
    edge_x = []
    edge_y = []
    for edge in graph.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_x.extend([x0, x1, None])
        edge_y.extend([y0, y1, None])

    # 绘制边
    edge_trace = go.Scatter(
        x=edge_x,
        y=edge_y,
        line=dict(width=1, color='#888'),
        hoverinfo='none',
        mode='lines'
    )

    # 提取节点的坐标
    node_x = [pos[node][0] for node in graph.nodes()]
    node_y = [pos[node][1] for node in graph.nodes()]
    node_text = list(graph.nodes())  # 节点标签

    # 绘制节点
    node_trace = go.Scatter(
        x=node_x,
        y=node_y,
        mode='markers+text',
        text=node_text,
        hoverinfo='text',
        marker=dict(
            showscale=True,
            colorscale='YlGnBu',
            size=20,
            colorbar=dict(
                thickness=15,
                title='节点颜色',
                xanchor='left',
                titleside='right'
            ),
            color=[len(graph[node]) for node in graph.nodes()]  # 根据连接数着色
        )
    )

    # 设置布局
    layout = go.Layout(
        title='交互式网络图',
        showlegend=False,
        hovermode='closest',
        margin=dict(b=0, l=0, r=0, t=30),
        xaxis=dict(showgrid=False, zeroline=False),
        yaxis=dict(showgrid=False, zeroline=False)
    )

    # 创建图
    fig = go.Figure(data=[edge_trace, node_trace], layout=layout)
    fig.show()


from datetime import datetime


def 为节点和边添加日期(图):
    """
    为图中的所有节点和边添加当前日期。
    :param 图: networkx 图对象
    """
    当前日期 = datetime.now().isoformat()  # 获取当前时间，格式为 ISO 8601

    # 为每个节点添加日期
    for 节点 in 图.nodes:
        属性 = 图.nodes[节点]["属性"]
        if len(属性) == 6:  # 如果节点尚未包含日期
            属性.append(当前日期)  # 添加日期
            图.nodes[节点]["属性"] = 属性

    # 为每条边添加创建日期
    for 边 in 图.edges:
        # 直接为边添加创建日期字段
        图.edges[边]["创建日期"] = 当前日期


if __name__ == "__main__":
    print(遍历边(记忆图))
    print(遍历节点(记忆图))
    保存图为_json(记忆图, "记忆图.pkl")
    显示交互式图(记忆图)
