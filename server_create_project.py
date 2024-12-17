from vempu_api import *

if __name__ == "__main__":

    user_name = "yhbian"
    project_name = "Multi_DateCenter_Experiment"

    backend_ip = "192.168.1.46"
    backend_port = 25890

    image_manager = ImageManager(user_name, backend_ip, backend_port)
    project_manager = ProjectManager(user_name, backend_ip, backend_port)
    node_manager = NodeManager(user_name, project_name, backend_ip, backend_port)
    link_manager = LinkManager(user_name, project_name, backend_ip, backend_port)
    cmd_manager = CmdManager(user_name, project_name, backend_ip, backend_port)
    images = ImageManager(user_name, backend_ip, backend_port).get_images()

    astra_image = images["astra-sim"]
    ubuntu_image = images["ubuntu"]
    ovs_image = images["ovs"]

    topo = Topo()

    h1 = topo.add_node(
        astra_image,
        node_name = "h1",
        location={"x":200, "y":200}
    )
    h2 = topo.add_node(
        astra_image, 
        node_name = "h2",
        location={"x":400, "y":200}
    )
    h3 = topo.add_node(
        astra_image,
        node_name = "h3",
        location={"x":200, "y":400}
    )
    h4 = topo.add_node(
        astra_image,
        node_name = "h4",
        location={"x":400, "y":400}
    )
    s1 = topo.add_node(
        ovs_image,
        node_name = "s1",
        location={"x":300, "y":300}
    )
    h5 = topo.add_node(
        ubuntu_image,
        node_name = "h5",
        location={"x":300, "y":600}
    )

    topo.add_link(h1, s1, link_name="l1", src_IP="192.168.1.1/24")
    topo.add_link(h2, s1, link_name="l2", src_IP="192.168.1.2/24")
    topo.add_link(h3, s1, link_name="l3", src_IP="192.168.1.3/24")
    topo.add_link(h4, s1, link_name="l4", src_IP="192.168.1.4/24")
    topo.add_link(h5, s1, link_name="l5", src_IP="192.168.1.5/24")

    project_manager.deploy(project_name, topo)
    print(f"Deploy {project_name} successfully! Please check the effect at the "
        "frontend! Sleep 20s...")
    

    src_link_config = LinkConfiguration(bw_kbps="10000000", delay_us="100"
        link="l1", ne="h1")
    dst_link_config = LinkConfiguration(bw_kbps="10000000", delay_us="100",
        link="l1", ne="s1")
    link_manager.config_link(src_link_config, dst_link_config)


    src_link_config = LinkConfiguration(bw_kbps="5000000", delay_us="150"
        link="l2", ne="h2")
    dst_link_config = LinkConfiguration(bw_kbps="5000000", delay_us="150",
        link="l2", ne="s1")
    link_manager.config_link(src_link_config, dst_link_config)

    src_link_config = LinkConfiguration(bw_kbps="10000000", delay_us="0"
        link="l3", ne="h3")
    dst_link_config = LinkConfiguration(bw_kbps="10000000", delay_us="0",
        link="l3", ne="s1")
    link_manager.config_link(src_link_config, dst_link_config)

    src_link_config = LinkConfiguration(bw_kbps="15000000", delay_us="100"
        link="l4", ne="h4")
    dst_link_config = LinkConfiguration(bw_kbps="15000000", delay_us="100",
        link="l4", ne="s1")
    link_manager.config_link(src_link_config, dst_link_config)

    src_link_config = LinkConfiguration(bw_kbps="10000000", delay_us="250"
        link="l5", ne="h5")
    dst_link_config = LinkConfiguration(bw_kbps="10000000", delay_us="250",
        link="l5", ne="s1")
    link_manager.config_link(src_link_config, dst_link_config)

    # 链路配置