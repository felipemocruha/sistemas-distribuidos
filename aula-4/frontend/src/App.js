import React, { useState, useEffect } from "react";
import { Layout, Menu, Table, Card } from 'antd';
import { GithubOutlined } from "@ant-design/icons";
import axios from 'axios'
import {notification} from 'antd'
import "antd/dist/antd.css";

const { Header, Content } = Layout;
const BASE_URL = "https://api.alcantara.cloud";

const columns = [
 {
   title: 'Username',
   dataIndex: 'username',
   key: 'username',
   render: username => <b>{username}</b>,
  },
  {
    title: 'Created At',
    dataIndex: 'created_at',
    key: 'created_at',
	render: ts => <>{new Date(ts * 1000).toString()}</>,
  },
]

const data = [
  {
	key: '1',
	username: "jose",
	created_at: 242353646453,
  },
  {
	key: '2',
	username: "sua tia",
	created_at: 3439585934,
  },
]

function App() {
  const [accounts, setAccounts] = useState([]);

  useEffect(() => {
	try {
       return axios.get(`${BASE_URL}/api/v1/accounts`)
        .then((response) => {
		  setAccounts(response.data)
		  console.log(response.data)
        }, (error) => {
          notification['error']({
            message: 'Erro!',
            description: 'Houve um problema ao requisitar os dados, tente novamente.',
          })
        })
    } catch(err) {
      notification['error']({
        message: 'Erro!',
        description: 'Houve um problema ao enviar os dados, tente novamente.',
      })
    }
  }, []);

  return (
	<Layout>
      <Header style={{ position: 'fixed', zIndex: 1, width: '100%' }}>
		<div className="logo" />
		<Menu theme="dark" mode="horizontal" defaultSelectedKeys={['2']}>
          <Menu.Item key="1" onClick={()=> window.open("https://github.com/felipemocruha/sistemas-distribuidos/tree/master/aula-4", "_blank")}><GithubOutlined /> GitHub</Menu.Item>
		</Menu>
      </Header>
      <Content className="site-layout" style={{ padding: '0 50px', marginTop: 64 }}>
		<div className="site-layout-background" style={{ padding: 24, minHeight: 380 }}>
		  <Card title="Comece uma conversa com seus colegas!">
			<Table columns={columns} dataSource={accounts} />
		  </Card>
		</div>
      </Content>
	</Layout>
  );
}

export default App;
