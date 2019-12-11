XML = """<?xml version="1.0" encoding="UTF-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android" android:versionCode="6" android:versionName="6.0" package="bmthx.god102409paperi">
  <application android:label="@7F070001" android:icon="@7F02000B">
    <activity android:label="@7F070001" android:name=".Begin">
      <intent-filter>
        <action android:name="android.intent.action.MAIN" />
        <category android:name="android.intent.category.LAUNCHER" />
      </intent-filter>
    </activity>
    <activity android:label="@7F070001" android:name=".MainLuck" />
    <activity android:label="@7F070001" android:name=".ThxWebGod" />
    <activity android:name="com.google.ads.AdActivity" android:configChanges="0x000000B0" />
  </application>
  <uses-sdk android:minSdkVersion="3" />
  <supports-screens android:anyDensity="true" />
  <uses-permission android:name="android.permission.INTERNET" />
  <uses-permission android:name="android.permission.ACCESS_NETWORK_STATE" />
  <uses-permission android:name="android.permission.SET_WALLPAPER" />
  <uses-permission android:name="android.permission.MOUNT_UNMOUNT_FILESYSTEMS" />
  <uses-permission android:name="android.permission.WRITE_EXTERNAL_STORAGE" />
</manifest>
"""

INVALID_ROOT = """<?xml version="1.0" encoding="UTF-8"?>
<droid xmlns:android="http://schemas.android.com/apk/res/android" android:versionCode="6" android:versionName="6.0" package="bmthx.god102409paperi">
  <uses-permission android:name="android.permission.INTERNET" />
</droid>
"""

DOC = {
    "text": "",
    "tag": "manifest",
    "attrs": {
        "versioncode": "6",
        "versionname": "6.0",
        "package": "bmthx.god102409paperi",
    },
    "_children": [
        {
            "text": "",
            "tag": "application",
            "attrs": {"icon": "@7f02000b", "label": "@7f070001"},
            "_children": [
                {
                    "text": "",
                    "tag": "activity",
                    "attrs": {"name": ".begin", "label": "@7f070001"},
                    "_children": [
                        {
                            "text": "",
                            "tag": "intent-filter",
                            "attrs": {},
                            "_children": [
                                {
                                    "text": "",
                                    "tag": "action",
                                    "attrs": {"name": "android.intent.action.main"},
                                    "_children": [],
                                },
                                {
                                    "text": "",
                                    "tag": "category",
                                    "attrs": {
                                        "name": "android.intent.category.launcher"
                                    },
                                    "_children": [],
                                },
                            ],
                        }
                    ],
                },
                {
                    "text": "",
                    "tag": "activity",
                    "attrs": {"name": ".mainluck", "label": "@7f070001"},
                    "_children": [],
                },
                {
                    "text": "",
                    "tag": "activity",
                    "attrs": {"name": ".thxwebgod", "label": "@7f070001"},
                    "_children": [],
                },
                {
                    "text": "",
                    "tag": "activity",
                    "attrs": {
                        "configchanges": "0x000000b0",
                        "name": "com.google.ads.adactivity",
                    },
                    "_children": [],
                },
            ],
        },
        {
            "text": "",
            "tag": "uses-sdk",
            "attrs": {"minsdkversion": "3"},
            "_children": [],
        },
        {
            "text": "",
            "tag": "supports-screens",
            "attrs": {"anydensity": "true"},
            "_children": [],
        },
        {
            "text": "",
            "tag": "uses-permission",
            "attrs": {"name": "android.permission.internet"},
            "_children": [],
        },
        {
            "text": "",
            "tag": "uses-permission",
            "attrs": {"name": "android.permission.access_network_state"},
            "_children": [],
        },
        {
            "text": "",
            "tag": "uses-permission",
            "attrs": {"name": "android.permission.set_wallpaper"},
            "_children": [],
        },
        {
            "text": "",
            "tag": "uses-permission",
            "attrs": {"name": "android.permission.mount_unmount_filesystems"},
            "_children": [],
        },
        {
            "text": "",
            "tag": "uses-permission",
            "attrs": {"name": "android.permission.write_external_storage"},
            "_children": [],
        },
    ],
}

FLAT = [
    {
        "text": "",
        "tag": "manifest",
        "attrs": {
            "versioncode": "6",
            "versionname": "6.0",
            "package": "bmthx.god102409paperi",
        },
    },
    {
        "text": "",
        "tag": "uses-permission",
        "attrs": {"name": "android.permission.write_external_storage"},
    },
    {
        "text": "",
        "tag": "uses-permission",
        "attrs": {"name": "android.permission.mount_unmount_filesystems"},
    },
    {
        "text": "",
        "tag": "uses-permission",
        "attrs": {"name": "android.permission.set_wallpaper"},
    },
    {
        "text": "",
        "tag": "uses-permission",
        "attrs": {"name": "android.permission.access_network_state"},
    },
    {
        "text": "",
        "tag": "uses-permission",
        "attrs": {"name": "android.permission.internet"},
    },
    {"text": "", "tag": "supports-screens", "attrs": {"anydensity": "true"}},
    {"text": "", "tag": "uses-sdk", "attrs": {"minsdkversion": "3"}},
    {
        "text": "",
        "tag": "application",
        "attrs": {"label": "@7f070001", "icon": "@7f02000b"},
    },
    {
        "text": "",
        "tag": "activity",
        "attrs": {"configchanges": "0x000000b0", "name": "com.google.ads.adactivity"},
    },
    {
        "text": "",
        "tag": "activity",
        "attrs": {"name": ".thxwebgod", "label": "@7f070001"},
    },
    {
        "text": "",
        "tag": "activity",
        "attrs": {"name": ".mainluck", "label": "@7f070001"},
    },
    {"text": "", "tag": "activity", "attrs": {"name": ".begin", "label": "@7f070001"}},
    {"text": "", "tag": "intent-filter", "attrs": {}},
    {
        "text": "",
        "tag": "category",
        "attrs": {"name": "android.intent.category.launcher"},
    },
    {"text": "", "tag": "action", "attrs": {"name": "android.intent.action.main"}},
]
