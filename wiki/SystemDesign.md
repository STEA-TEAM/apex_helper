## Overview

```mermaid
classDiagram
    direction TB
    class ImageProvider {
        -DXCamera __camera
        -Dict[str, ImageConsumer] __consumers
    }
    ImageProvider <.. ImageProvider: Thread Loop
    class ImageConsumer {
        <<Abstract>>
        #Image _current_image
        +feed(image: Image)
        +@abstract process()
    }
    ImageConsumer <.. ImageConsumer: Thread Loop
    ImageProvider *-- ImageConsumer
    class EnemyBroadcaster {
        +@override process()
    }
    class ItemBroadcaster {
        +@override process()
    }
    class WeaponBroadcaster {
        -ImageDebugger __debugger
        -Dict[str, WeaponSubscriber] __subscribers
        +@override process()
    }
    ImageConsumer <|-- EnemyBroadcaster
    ImageConsumer <|-- ItemBroadcaster
    ImageConsumer <|-- WeaponBroadcaster
    class WeaponSubscriber {
        #AmmoInfo _current_ammo_info
        #str _current_weapon_identity
        +notify(ammo_info: AmmoInfo, weapon_identity: str)
    }
    WeaponBroadcaster *-- WeaponSubscriber

    class InputProvider {
        -Listener __listener
        -Dict[str, InputConsumer] __consumers
    }
    InputProvider <.. InputProvider: Thread Loop
    class MonoTasker {
        <<Abstract>>
        +trigger(input_info: InputInfo)
        +@abstract abort()
        #@abstract _start()
    }
    MonoTasker <.. MonoTasker: Thread Loop
    InputProvider *-- MonoTasker

    class RecoilSuppressor {
        -Dict[str, BaseAdapter] __adapters
        +@override abort()
        #@override _start()
    }
    WeaponSubscriber <|-- RecoilSuppressor
    MonoTasker <|-- RecoilSuppressor
    class BaseAdapter {
        <<Abstract>>
        -List[Tuple[DeviceType, DeviceEvent, float]] __events
        +push_events(events: List[Tuple[DeviceType, DeviceEvent, float]])
        +replace_events(events: List[Tuple[DeviceType, DeviceEvent, float]], force: bool)
        +@abstract process(device_type: DeviceType, device_event: DeviceEvent)
    }
    BaseAdapter <.. BaseAdapter: Thread Loop
    RecoilSuppressor *-- BaseAdapter
    class EmulateAdapter {
        +@override process()
    }
    class HidAdapter {
        -HidDevice __hid
        +@override process()
    }
    BaseAdapter <|-- EmulateAdapter
    BaseAdapter <|-- HidAdapter
```

## References

### Tools

- [Apex Legends Calculator](https://jscalc.io/embed/Q1gf45VCY4tmm2dq)
- [Mouse Sensitivity Calculator](https://www.mouse-sensitivity.com/?share=598ee2e60b31d9226578d809f7380a09)

### Articles

- [Apex Legends Calculator blog](https://jscalc-blog.com/apex-legends-calculator/)