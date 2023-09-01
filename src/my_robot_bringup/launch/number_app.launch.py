from launch import LaunchDescription
from launch_ros.actions import Node  #node eklemek için

def generate_launch_description():
    ld = LaunchDescription()

    remap_number_topic = ("number", "my_number")  # Topic için yeni isim oluşturma (eski_ad, yeni_ad)

    number_publisher_node = Node(    #node oluşturup içerisine verileri giriyorsun.
        package="my_py_pkg",         #bağlayacağın paketin adını giriyorsun.
        executable="number_publisher", #yürütülebilir dosya adını giriyorsun setup.py daki
        name="my_number_publisher", #node un ismini değiştirmek için kullanılır
        remappings=[
            remap_number_topic
        ],   #virgülü unutma!!!!

        parameters=[
            {"number_to_publish":4}
        ]
    )

    number_counter_node = Node(
        package="my_py_pkg",
        executable="number_counter",
        name="my_number_counter",
        remappings=[
            remap_number_topic,
            ("number_count","my_number_count")
        ]
    )

    ld.add_action(number_publisher_node)  #bağlayarak oluşturduğun nodeları çalıştırıyorsun
    ld.add_action(number_counter_node)

    return ld
