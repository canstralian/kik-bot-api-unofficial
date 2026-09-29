> **Historical reference only:** These examples document older observed message shapes, not current Kik compatibility. Identifiers, personal text, media tokens, CAPTCHA material and encoded payloads have been replaced with placeholders. Never use this page as a source of live authentication artifacts or test-account credentials.

The following message formats are examples of how kik's language (or XMPP elements) actually look like.

This page is useful when you just want to have an idea of what certain events look like in XMPP, or you want to support a type of event which is not implemented yet by the API.

The following events were contributed by: [maritaria](https://github.com/maritaria), [Jaapp](https://github.com/Jaapp-), [LynxKik](https://github.com/LynxKik).

## General ##

Receiving a delivery notification for a sent message:

```xml
<message type="receipt" id="[GUID]" xmlns="jabber:client" to="[BOT_JID]@talk.kik.com" from="[USER_JID]@talk.kik.com">
	<receipt type="delivered" xmlns="kik:message:receipt">
		<msgid id="[MESSAGE_ID]"/>
	</receipt>
	<kik app="chat" push="false" timestamp="1511183559656" qos="true" hop="true"/>
	<g jid="[GROUP_JID]@groups.kik.com"/>
</message>
```

Receiving a read notification for a sent message:

```xml
<message from="[USER_JID]@talk.kik.com" to="[BOT_JID]@talk.kik.com" type="receipt" cts="1511183930239" xmlns="jabber:client" id="[GUID]">
	<kik qos="true" timestamp="1511183930239" push="false" hop="true" app="chat"/>
	<receipt xmlns="kik:message:receipt" type="read">
		<msgid id="[MESSAGE_ID_1]"/>
		<msgid id="[MESSAGE_ID_2]"/>
		<msgid id="[MESSAGE_ID_3]"/>
		<msgid id="[MESSAGE_ID_4]"/><!-- you can receive multiple at a time -->
	</receipt><g jid="[GROUP_JID]@groups.kik.com"/>
</message>
```

Requesting the roster (the groups and people you are chatting with):

```xml
<iq type="get" id="[GUID]">
	<query p="8" xmlns="jabber:iq:roster" />
</iq>
```

Response to requesting roster:

```xml
<iq to="[BOT_JID]@talk.kik.com/CAN167da12427ee4dc4a36b40e8debafc25" type="result" id="[REQUEST_GUID]">
	<query ts="1511180666000" xmlns="jabber:iq:roster">
		<g is-public="true" jid="[GROUP_JID]@groups.kik.com">
			<code>#[GROUP_HASHTAG]</code>
			<n>[GROUP_DISPLAY_NAME]</n>
			<pic ts="1505911808105">http://profilepics.cf.kik.com/[SOME_IDENTIFIER]</pic>
			<m s="1" a="1">[USER_JID]@talk.kik.com</m><!-- owner -->
			<m a="1">[USER_JID]@talk.kik.com</m><!-- admin -->
			<m>[USER_JID]@talk.kik.com</m><!-- user -->
			<!-- users are listed here until the end -->
		</g>
		<!-- all other groups follow the same format and appear before the users are listed -->
		<item jid="kikteam@talk.kik.com">
			<username>kikteam</username>
			<display-name>Kik Team</display-name>
			<pic ts="1479751536620">https://profilepics.cf.kik.com/[REDACTED]</pic>
			<verified/><!-- indicates the user has a purple gear -->
			<pubkey/>
		</item>
	</query>
</iq>
```

Removing a friend using their JabberID:

```xml
<iq type="set" id="[GUID]">
	<query xmlns="kik:iq:friend">
		<remove jid="[FRIEND_JID]" />
	</query>
</iq>
```

Response:

```xml
<iq to="[BOT_JID]" id="[GUID_FROM_REQUEST]" type="result">
	<query status="ok" xmlns="kik:iq:friend"/>
</iq>
```
_According to the code the request is succesfull if `status` is equal to `ok`, otherwise it has failed._

## Group messeging ##

When your bot gets added to a group (the bot has chatted with the inviter, so it gets added immediately):

```xml
<message from="[NUMBERS]_g@groups.kik.com" to="[BOT_JID]" type="groupchat" id="[GUID]" xmlns="jabber:client">
    <kik qos="true" app="all" hop="true" timestamp="1510865418472" push="false"/>
    <request d="false" r="false" xmlns="kik:message:receipt"/>
    <roster/>
    <g is-public="true" jid="[NUMBERS]_g@groups.kik.com"><!-- NUMBERS same as message.from -->
        <code>#[PUBLIC_GROUP_HASH]</code>
        <n>Bot testing ground</n>
        <pic ts="1505911808105">http://profilepics.cf.kik.com/[REDACTED]</pic>
        <m>[JID]@talk.kik.com</m><!-- The jid of the bot is also in the list -->
        <m>[JID]@talk.kik.com</m><!-- Some other member -->
        <m s="1" a="1">[JID]@talk.kik.com</m><!-- Owner account, S=owner A=admin -->
    </g>
    <sysmsg xmlns="kik:msg:info">[FIRSTNAME] [LASTNAME] has added you to the chat</sysmsg>
</message>
```

Sending a message in a group:

```xml
<message type="groupchat" to="[GROUP_JID]@groups.kik.com" id="[GUID]" cts="1511183566420"><!-- id is MESSAGE_ID later on -->
	<body>[MESSAGE_TO_SEND]</body>
	<pb></pb>
	<preview></preview><!-- this doesnt matter -->
	<kik push="true" qos="true" timestamp="1511183566420" />
	<request xmlns="kik:message:receipt" r="true" d="true" /><!-- r: receive read request d: receive delivery request -->
	<ri/>
</message>
```

When someone sends a message in a group:

```xml
<message id="[GUID]" type="groupchat" cts="1510911505345" xmlns="kik:groups" from="[USER_JID]@talk.kik.com" to="[BOT_JID]@talk.kik.com">
	<body>[SYNTHETIC_GROUP_MESSAGE]</body><!-- This is the original message as captured during the test -->
	<pb/>
	<preview>[SYNTHETIC_PREVIEW]</preview><!-- some shortened version of the body -->
	<kik timestamp="1510911505345" push="true" app="chat" qos="true" hop="true"/>
	<request d="true" r="true" xmlns="kik:message:receipt"/>
	<ri/>
	<g jid="[GROUP_JID]@groups.kik.com"/><!-- group the message was posted in -->
</message>
```

When someone starts or is typing:

```xml
<message id="[GUID]" type="groupchat" xmlns="kik:groups" from="[TYPING_USER_JID]@talk.kik.com" to="[BOT_JID]@talk.kik.com">
	<pb/>
	<kik timestamp="1510911793198" push="false" app="chat" qos="false" hop="true"/>
	<is-typing val="true"/>
	<g jid="[GROUP_JID]@groups.kik.com"/><!-- the group the user is typing in -->
</message>
```

When someone stops typing:

```xml
<message id="[GUID]" type="groupchat" xmlns="kik:groups" from="[TYPING_USER_JID]@talk.kik.com" to="[BOT_JID]@talk.kik.com">
	<pb/>
	<kik timestamp="1510911793414" push="false" app="chat" qos="false" hop="true"/>
	<is-typing val="false"/>
	<g jid="[GROUP_JID]@groups.kik.com"/>
</message>
```

Receiving an image taken with the kik camera in a group chat:

```xml
<message from="[USER_JID]@talk.kik.com" cts="1511197075873" to="[BOT_JID]@talk.kik.com" id="[GUID]" xmlns="kik:groups" type="groupchat">
	<pb/>
	<kik push="true" hop="true" app="chat" timestamp="1511197075873" qos="true"/>
	<request r="true" xmlns="kik:message:receipt" d="true"/>
	<content app-id="com.kik.ext.camera" id="[GUID]" v="2">
		<strings>
			<app-name>Camera</app-name>
			<file-size>49656</file-size>
			<allow-forward>true</allow-forward>
			<file-content-type>image/jpeg</file-content-type>
			<file-name>[GUID from content#id].jpg</file-name>
			<file-url>https://platform.kik.com/content/files/[GUID from content#id]?t=[KEY]</file-url>
		</strings>
		<extras/>
		<hashes>
			<sha1-original>B00C270632D11ECE461A487052394975A47EAA28</sha1-original>
			<sha1-scaled>E5CDB95540F7ADE7801CA152CC8C33227ABCEA92</sha1-scaled>
			<blockhash-scaled>00000001FFFEFF7F03A0FFFEFFF00000FFFFEFC700030010000F3FFFFC03001F</blockhash-scaled>
		</hashes>
		<images>
			<preview>LARGE_BLOB_OF_DATA</preview>
			<icon>LARGE_BLOB_OF_DATA</icon>
		</images>
		<uris/>
	</content><g jid="[GROUP_JID]@groups.kik.com"/>
</message>
```

Receiving a gallery image in a group chat:

```xml
<message from="[USER_JID]@talk.kik.com" cts="1511197087988" to="[BOT_JID]@talk.kik.com" id="[GUID]" xmlns="kik:groups" type="groupchat">
	<pb/>
	<kik push="true" hop="true" app="chat" timestamp="1511197087988" qos="true"/>
	<request r="true" xmlns="kik:message:receipt" d="true"/>
	<content app-id="com.kik.ext.gallery" id="[GUID]" v="2">
		<strings>
			<app-name>Gallery</app-name>
			<file-size>171087</file-size>
			<allow-forward>true</allow-forward>
			<file-name>[GUID from content#id].jpg</file-name>
			<file-url>https://platform.kik.com/content/files/[GUID from content#id]?t=[KEY]</file-url>
		</strings>
		<extras/>
		<hashes>
			<sha1-scaled>EC3C7C23B00F84010B33754AC7E51FCD26E630A3</sha1-scaled>
			<blockhash-scaled>FFFE00000000FFFF00001F101FFE3FFE1FE00FF807F803F01FFE0FFC07F80040</blockhash-scaled>
			<sha1-original>9AE9130EE3BB5CCC7F8D449B5BD778D4A916BD6C</sha1-original>
		</hashes>
		<images>
			<preview>LARGE_BLOB_OF_DATA</preview>
			<icon>LARGE_BLOB_OF_DATA</icon>
		</images>
		<uris/>
	</content><g jid="[GROUP_JID]@groups.kik.com"/>
</message>
```
_Note: the image urls can be opened in a browser without further authentication_

Receiving a sticker (in a group chat):

```xml
<message cts="1511347191450" id="[GUID]" xmlns="kik:groups" to="[BOT_JID]" from="[USER_JID]" type="groupchat">
	<pb/>
	<kik qos="true" hop="true" timestamp="1511347191450" app="chat" push="true"/>
	<request d="true" r="true" xmlns="kik:message:receipt"/>
	<content v="2" app-id="com.kik.ext.stickers" id="dbffd5eb-3f4d-43d8-b240-2ad0379e9ec1">
		<strings>
			<app-name>Stickers</app-name>
			<attribution/>
			<layout>photo</layout>
			<video-should-loop>false</video-should-loop>
			<video-should-autoplay>false</video-should-autoplay>
			<disallow-save>false</disallow-save>
			<video-should-be-muted>false</video-should-be-muted>
			<title/>
			<text/>
			<allow-forward>false</allow-forward>
		</strings>
		<extras>
			<item>
				<key>sticker_pack_id</key>
				<val>cosmocat</val>
			</item>
			<item>
				<key>sticker_url</key>
				<val>https://cdn.kik.com/stickersv2/packs/cosmocat/05.png</val>
			</item>
			<item>
				<key>sticker_id</key>
				<val>5946604915261440</val>
			</item>
			<item>
				<key>sticker_source</key>
				<val>Pack</val>
			</item>
		</extras>
		<hashes/>
		<images>
			<png-preview>BASE64_BLOB</png-preview>
		</images>
		<uris>
			<uri platform="com.kik.ext.stickers">https://stickers.kik.com/</uri>
			<uri platform="cards">https://stickers.kik.com/</uri>
		</uris>
	</content>
	<g jid="[GROUP_JID]"/>
</message>
```

Receiving a message from a bot with an embedded keyboard (reply label below the message bubble):

```xml
<!-- someone summoning the bot-->
<message cts="1511347420147" id="[GUID]" xmlns="kik:groups" to="[YOUR_BOT_JID]" from="[USER_JID]" type="groupchat">
	<body>@examplebot Who's lurking? (10 secs)</body>
	<mention>
		<bot>[EXAMPLE_BOT_JID]</bot>
	</mention>
	<pb>[BASE64_BLOB]</pb>
	<preview>@whoslurki...</preview>
	<kik qos="true" hop="true" timestamp="1511347420147" app="chat" push="true"/>
	<request d="true" r="true" xmlns="kik:message:receipt"/>
	<g jid="[GROUP_JID]"/>
</message>
<!-- bot reply -->
<message cts="1511347420713" id="[GUID]" xmlns="jabber:client" to="[YOUR_BOT_JID]" from="[EXAMPLE_BOT_JID]" type="groupchat">
	<kik qos="true" hop="true" timestamp="1511347420713" app="chat" push="true"/>
	<request d="true" r="true" xmlns="kik:message:receipt"/>
	<body>Calculating who's lurking... please click get results in a 10 seconds!</body>
	<g jid="[GROUP_JID]"/>
	<pb>BASE64_BLOB</pb>
	<suggested-responses hidden="false">
		<text>Who&apos;s lurking? (10 secs)</text>
		<text>Who&apos;s lurking? (30 secs)</text>
		<text>Who&apos;s lurking? (60 secs)</text>
		<text>Get results</text>
		<text>Help</text>
	</suggested-responses>
</message>
```

When someone leaves a (public) group your bot is a member of:

```xml
<message type="groupchat" xmlns="jabber:client" id="[GUID]" from="[NUMBERS]_g@groups.kik.com" to="[BOT_JID]@talk.kik.com"><!-- JID of group -->
	<kik timestamp="1510911460608" push="false" app="all" qos="true" hop="true"/>
	<request d="false" r="false" xmlns="kik:message:receipt"/>
	<roster/>
	<g jid="[NUMBERS]_g@groups.kik.com"> <!-- JID of group -->
		<l>[USER_JID]@talk.kik.com</l><!-- JID of user that left -->
	</g>
	<status jid="[USER_JID]@talk.kik.com">[FIRSTNAME] [LASTNAME] has left the chat</status>
</message>
```

## History Retrieval ##

These are the messages for obtaining history. It happens in a loop.

1. This request is sent
```xml
<iq type="set" id="[GUID]" cts="1513349802685">
    <query xmlns="kik:iq:QoS">
	<msg-acks />
	<history attach="true" />
    </query>
</iq>
```

2. Within the "history" tag regular messages are sent with "msg" tags (those are "message" tags in our current parsing code).
```xml
<iq type="result" id="[GUID]" from="warehouse@talk.kik.com" to="[USER_JID]@talk.kik.com/...">
    <query xmlns="kik:iq:QoS">
	<history more="1" attach="true">
	    <msg type="receipt" id="[MESSAGE_ID]" from="[EXAMPLE_SENDER_JID]">
		<kik app="chat" push="false" timestamp="1511036055842" qos="true"/>
		<receipt type="read" xmlns="kik:message:receipt">
		    <msgid id="[MESSAGE_ID]"/>
		</receipt>
	    </msg>
	    <msg type="chat" id="[GUID]" from="[USER_JID]@talk.kik.com">
		<body>[SYNTHETIC_CHAT_TEXT]</body>
		<pb/>
		<preview>[SYNTHETIC_PREVIEW]</preview>
		<kik app="chat" push="true" timestamp="1511036150972" qos="true"/>
		<request d="true" xmlns="kik:message:receipt" r="true"/>
		<ri/>
	    </msg>
	    <msg type="groupchat" id="[GUID]" from="[USER_JID]@talk.kik.com">
		<body>[SYNTHETIC_CHAT_TEXT]</body>
		<pb/>
		<preview>[SYNTHETIC_PREVIEW]</preview>
		<kik app="chat" push="true" timestamp="1511036907685" qos="true"/>
		<request d="true" xmlns="kik:message:receipt" r="true"/>
		<ri/>
		<g jid="[GROUP_JID]_g@groups.kik.com"/>
	    </msg>
	</history>
	<polling interval="60"/>
    </query>
</iq>
```
3. When calling the first request again, the same response is sent. To get the next chunk of history, acks are sent for each message of the last chunk, along with the new history request.
```xml
<iq type="set" id="[GUID]" cts="1513349804653">
    <query xmlns="kik:iq:QoS">
	<msg-acks>
	    <sender jid="[USER_JID]@talk.kik.com">
		<ack-id receipt="false">[MESSAGE_ID]</ack-id>
		<ack-id receipt="true">[MESSAGE_ID]</ack-id>
	    </sender>
	    <sender jid="[USER_JID]@talk.kik.com"  g="[GROUP_JID]_g@groups.kik.com">
		<ack-id receipt="false">[MESSAGE_ID]</ack-id>
		<ack-id receipt="true">[MESSAGE_ID]</ack-id>
	    </sender>
	</msg-acks>
	<history attach="true" />
    </query>
</iq>
```

## Group adminship ##

Add people to a group:

```xml
<iq type="set" id="[GUID]">
    <query xmlns="kik:groups:admin">
	<g jid="[GUID]">
	    <m>[USER_JID_1]@talk.kik.com</m>
            <m>[USER_JID_2]@talk.kik.com</m>
	</g>
    </query>
</iq>
```

Remove someone from group:

```xml
<iq type="set" id="[GUID]">
    <query xmlns="kik:groups:admin">
	<g jid="[GUID]">
	    <m r="1">[USER_JID]@talk.kik.com</m>
	</g>
    </query>
</iq>
```
Change the group name:

```xml
<iq type="set" id="[GUID]">
    <query xmlns="kik:groups:admin">
	<g jid="[GUID]">
	    <n>[GROUPNAME]</n>
	</g>
    </query>
</iq>
```

Ban:

```xml
<iq type="set" id="[GUID]">
    <query xmlns="kik:groups:admin">
	<g jid="[GUID]">
	    <b>[USER_JID]@talk.kik.com</b>
	</g>
    </query>
</iq>
```

Unban:

```xml
<iq type="set" id="[GUID]">
    <query xmlns="kik:groups:admin">
	<g jid="[GUID]">
	    <b r="1">[USER_JID]@talk.kik.com</b>
	</g>
    </query>
</iq>
```

_Banned members are listed with \<b\>[JID]\</b\> instead of \<m\>._

Notification message when another admin has unbanned a member:

```xml
<message id="[GUID]" to="[BOT_JID]" type="groupchat" xmlns="jabber:client" from="[GROUP_JID]">
	<kik qos="true" timestamp="1511359715596" app="all" push="false" hop="true"/>
	<request r="false" d="false" xmlns="kik:message:receipt"/>
	<roster/>
	<g jid="[GROUP_JID]"/>
	<status jid="[UNBANNED_USER_JID]">[FIRSTNAME] [LASTNAME] has unbanned [FIRSTNAME]
 [LASTNAME]</status>
</message>
```

When someone makes you admin:

```xml
<message type="groupchat" to="[BOT_JID]@talk.kik.com" xmlns="jabber:client" id="[GUID]" from="[GROUP_JID]@groups.kik.com">
	<kik hop="true" push="false" app="all" qos="true" timestamp="1511180642944"/>
	<request d="false" r="false" xmlns="kik:message:receipt"/>
	<roster/>
	<g jid="[GROUP_JID]@groups.kik.com"/>
	<sysmsg xmlns="kik:msg:info">You have been promoted to admin by [ADMIN_FIRSTNAME] [ADMIN_LASTNAME]</sysmsg>
</message>
```

When the owner of a group removes your adminship:

```xml
<message type="groupchat" to="[BOT_JID]@talk.kik.com" xmlns="jabber:client" id="[GUID]" from="[GROUP_JID]@groups.kik.com">
	<kik hop="true" push="false" app="all" qos="true" timestamp="1511180665857"/>
	<request d="false" r="false" xmlns="kik:message:receipt"/>
	<roster/>
	<g jid="[GROUP_JID]@groups.kik.com"/>
	<sysmsg xmlns="kik:msg:info">Your admin status has been removed by [ADMIN_FIRSTNAME] [ADMIN_LASTNAME]</sysmsg>
</message>
```

Request to make another member an admin:

```xml
<iq type="set" id="[GUID]">
	<query xmlns="kik:groups:admin">
		<g jid="[GROUP_JID]">
			<m a="1">[USER_JID]</m>
		</g>
	</query>
</iq>

```

Response when the bot is an admin and the target user is in the group:

```xml
<iq to="[BOT_JID]" type="result" id="[GUID]">
	<query xmlns="kik:groups:admin"/>
</iq>
```
_The request also succeeds if the user is already an admin_

Response when the bot is not an admin:

```xml
<iq to="[BOT_JID]" type="error" id="[GUID]">
	<query xmlns="kik:groups:admin"><!-- the server echo's back the request as well -->
		<g jid="[GROUP_JID]">
			<m a="1">[TARGET_USER_JID]</m>
		</g>
	</query>
	<error type="modify" code="400">
		<bad-request xmlns="urn:ietf:params:xml:ns:xmpp-stanzas"/>
		<not-admin/>
	</error>
</iq>
```
_According to the code the request has succeded if one of the following nodes are *not* present in the response before reaching the closing `</iq>`:_ `<not-authorized/>` (_The bot is not authorized_), `<not-member/>` _(The target member is not in the group)_, `<bad-request/>`

Request to remove admin privileges from (demote) someone:

```xml
<iq type="set" id="[GUID]">
    <query xmlns="kik:groups:admin">
	<g jid="[GUID]">
	    <m a="0">[USER_JID]@talk.kik.com</m>
	</g>
    </query>
</iq>
```

## Registration ##

Validating first/last name when registering:
```xml
<iq type="get" id="[GUID]">
    <query xmlns="kik:iq:check-unique">
	<first>[FIRST_NAME]</first>
	<last>[LAST_NAME]</last>
    </query>
</iq>
```

Response for validating first/last name:
```xml
<iq id="[GUID]" type="result">
    <query xmlns="kik:iq:check-unique">
	<first is-valid="[GUID]">[FIRST_NAME]</first>
	<last is-valid="[GUID]">[LAST_NAME]</last>
    </query>
</iq>
```

Validating username:

```xml
<iq type="get" id="[GUID]">
    <query xmlns="kik:iq:check-unique">
	<username>[USER_NAME]</username>
    </query>
</iq>
````
Response for validating username:

```xml
<iq id="[GUID]" type="result">
    <query xmlns="kik:iq:check-unique">
	<username is-unique="false">[USER_NAME]</username>
    </query>
</iq>
```

Registering an account without captcha:

```xml
<iq type="set" id="[GUID]">
    <query xmlns="jabber:iq:register">
	<email>[EMAIL]</email>
	<passkey-e>[PASSKEY_E]</passkey-e>
	<passkey-u>[PASSKEY_U]</passkey-u>
	<device-id>[DEVICE_ID]</device-id>
	<username>[USERNAME]</username>
	<first>[FIRST_NAME]</first>
	<last>[LAST_NAME]</last>
	<birthday>1974-11-20</birthday>
	<version>11.38.0.18991</version>
	<device-type>android</device-type>
	<model>Nexus 7</model>
	<android-sdk>25</android-sdk>
	<registrations-since-install>1</registrations-since-install>
	<install-date>unknown</install-date>
	<logins-since-install>0</logins-since-install>
	<prefix>CAN</prefix>
	<lang>en_US</lang>
	<brand>google</brand>
	<android-id>[ANDROID_ID]</android-id>
    </query>
</iq>
```

Response for registering an account without captcha:
```xml
<iq id="[GUID]" type="error">
    <query xmlns="jabber:iq:register">
	<email>[EMAIL]</email>
	<passkey-e>[PASSKEY_E]</passkey-e>
	<passkey-u>[PASSKEY_U]</passkey-u>
	<device-id>[DEVICE_ID]</device-id>
	<username>[USERNAME]</username>
	<first>[FIRST_NAME]</first>
	<last>[LAST_NAME]</last>
	<birthday>1974-11-20</birthday>
	<version>11.38.0.18991</version>
	<device-type>android</device-type>
	<model>Nexus 7</model>
	<android-sdk>25</android-sdk>
	<registrations-since-install>1</registrations-since-install>
	<install-date>unknown</install-date>
	<logins-since-install>0</logins-since-install>
	<prefix>CAN</prefix>
	<lang>en_US</lang>
	<brand>google</brand>
	<android-id>[ANDROID_ID]</android-id>
    </query>
    <error code="406" type="modify">
	<not-acceptable xmlns="urn:ietf:params:xml:ns:xmpp-stanzas"/>
	<challenge xmlns="kik:challenge">
	    <captcha-type>web</captcha-type>
	    <captcha-url>https://captcha.kik.com/?id=[REDACTED]</captcha-url>
	    <captcha-challenge-id>[REDACTED_CHALLENGE_ID]</captcha-challenge-id>
	</challenge>
    </error>
</iq>
```

Registering an account with filled-in captcha:

```xml
<iq type="set" id="[GUID]">
    <query xmlns="jabber:iq:register">
	<email>[EMAIL]</email>
	<passkey-e>[PASSKEY_E]</passkey-e>
	<passkey-u>[PASSKEY_U]</passkey-u>
	<device-id>[DEVICE_ID]</device-id>
	<username>[USERNAME]</username>
	<first>[FIRST_NAME]</first>
	<last>[LAST_NAME]</last>
	<birthday>1974-11-20</birthday>
	<challenge>
	    <response>[REDACTED_CAPTCHA_RESPONSE]</response>
	</challenge>
	<version>11.38.0.18991</version>
	<device-type>android</device-type>
	<model>Nexus 7</model>
	<android-sdk>25</android-sdk>
	<registrations-since-install>1</registrations-since-install>
	<install-date>unknown</install-date>
	<logins-since-install>0</logins-since-install>
	<prefix>CAN</prefix>
	<lang>en_US</lang>
	<brand>google</brand>
	<android-id>[ANDROID_ID]</android-id>
    </query>
</iq>
```

Response for registering an account with captcha:

```xml
<iq id="[GUID]" type="result">
    <query xmlns="jabber:iq:register">
	<node>[USERNAME]_53w</node>
	<xiphias>
	    <response method="GetParticipatingExperiments" service="mobile.abtesting.v1.AbTesting">
		<body>[REDACTED_ENCODED_PAYLOAD]</body>
	    </response>
	</xiphias>
    </query>
</iq>
```
