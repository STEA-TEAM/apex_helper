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
    class InputConsumer {
        <<Abstract>>
        #InputInfo _current_input
        +feed(input_info: InputInfo)
        +@abstract process()
    }
    InputConsumer <.. InputConsumer: Thread Loop
    InputProvider *-- InputConsumer

    class RecoilSuppressor {
        -Dict[str, DeviceAdapter] __adapters
        +@override process()
    }
    WeaponSubscriber <|-- RecoilSuppressor
    InputConsumer <|-- RecoilSuppressor
    class DeviceAdapter {
        <<Abstract>>
        -List[DeviceEvent] __events
        +push_events(events: List[DeviceEvent])
        +replace_events(events: List[DeviceEvent], force: bool)
        +@abstract process()
    }
    DeviceAdapter <.. DeviceAdapter: Thread Loop
    RecoilSuppressor *-- DeviceAdapter
    class MouseEmulator {
        -MouseController __mouse
        +@override process()
    }
    class KeyboardEmulator {
        -KeyboardController __keyboard
        +@override process()
    }
    class MouseCommunicator {
        -HidDevice __hid
        +@override process()
    }
    class KeyboardCommunicator {
        -HidDevice __hid
        +@override process()
    }
    DeviceAdapter <|-- MouseEmulator
    DeviceAdapter <|-- KeyboardEmulator
    DeviceAdapter <|-- MouseCommunicator
    DeviceAdapter <|-- KeyboardCommunicator
```

## References

### Tools

- [Apex Legends Calculator](https://jscalc.io/embed/Q1gf45VCY4tmm2dq)
- [Mouse Sensitivity Calculator](https://www.mouse-sensitivity.com/?share=598ee2e60b31d9226578d809f7380a09)

### Articles

- [Apex Legends Calculator blog](https://jscalc-blog.com/apex-legends-calculator/)