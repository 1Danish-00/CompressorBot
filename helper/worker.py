#    This file is part of the Compressor distribution.
#    Copyright (c) 2021 Danish_00
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, version 3.
#
#    This program is distributed in the hope that it will be useful, but
#    WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
#    General Public License for more details.
#
#    License can be found in < https://github.com/1Danish-00/CompressorBot/blob/main/License> .

from .funcn import *


async def screenshot(e):
    await e.edit("`Generating Screenshots...`")
    COUNT.append(e.chat_id)
    wah = e.pattern_match.group(1).decode("UTF-8")
    key = decode(wah)
    out, dl, thum, dtime = key.split(";")
    os.mkdir(wah)
    tsec = await genss(dl)
    fps = 10 / tsec
    ncmd = f"ffmpeg -i '{dl}' -vf fps={fps} -vframes 10 '{wah}/pic%01d.png'"
    process = await asyncio.create_subprocess_shell(
        ncmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await process.communicate()
    er = stderr.decode()
    es = stdout.decode()
    pic = glob.glob(f"{wah}/*")
    await e.client.send_file(e.chat_id, pic)
    await e.client.send_message(
        e.chat_id,
        "Check Screenshots Above 😁",
        buttons=[
            [
                Button.inline("GENERATE SAMPLE", data=f"gsmpl{wah}"),
                Button.inline("COMPRESS", data=f"sencc{wah}"),
            ],
            [Button.inline("SKIP", data=f"skip{wah}")],
        ],
    )
    COUNT.remove(e.chat_id)
    shutil.rmtree(wah)


async def stats(e):
    wah = e.pattern_match.group(1).decode("UTF-8")
    wh = decode(wah)
    out, dl, thum, dtime = wh.split(";")
    ou = out.split("/")[-1]
    oo = out.replace(ou, "")
    pp = dl.split("/")[-1]
    dd = dl.replace(pp, "")
    ot = hbs(int(Path(out).stat().st_size))
    ov = hbs(int(Path(dl).stat().st_size))
    ans = f"Downloaded:\n{ov}\n\nCompressing:\n{ot}"
    try:
        await e.answer(ans, cache_time=0, alert=True)
    except:
        f = await e.reply(ans)
        await asyncio.sleep(3)
        await f.delete()


async def encc(e):
    es = dt.now()
    COUNT.append(e.chat_id)
    wah = e.pattern_match.group(1).decode("UTF-8")
    wh = decode(wah)
    out, dl, thum, dtime = wh.split(";")
    nn = await e.edit(
        "`Compressing..`",
        buttons=[
            [Button.inline("STATS", data=f"stats{wah}")],
            [Button.inline("CANCEL PROCESS", data=f"skip{wah}")],
        ],
    )
    cmd = f"ffmpeg -i '{dl}' -preset ultrafast -vcodec libx265 -crf 28 '{out}' -y"
    process = await asyncio.create_subprocess_shell(
        cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await process.communicate()
    er = stderr.decode()
    try:
        if er:
            await e.edit(str(er) + "\n\n**ERROR** Contact @danish_00")
            return
    except:
        pass
    o = stdout.decode()
    ees = dt.now()
    ttt = time.time()
    await nn.delete()
    nnn = await e.client.send_message(e.chat_id, "`Uploading...`")
    ds = await e.client.send_file(
        e.chat_id,
        file=f"{out}",
        force_document=True,
        thumb=thum,
        progress_callback=lambda d, t: asyncio.get_event_loop().create_task(
            progress(d, t, nnn, ttt, "uploading..", file=f"{out}")
        ),
    )

    org = int(Path(dl).stat().st_size)
    com = int(Path(out).stat().st_size)
    pe = 100 - ((com / org) * 100)
    per = str(f"{pe:.2f}") + "%"
    eees = dt.now()
    x = dtime
    xx = ts(int((ees - es).seconds) * 1000)
    xxx = ts(int((eees - ees).seconds) * 1000)
    dk = await ds.reply(
        f"Original Size : {hbs(org)}\nCompressed Size : {hbs(com)}\nCompressed Percentage : {per}\n\nDownloaded in {x}\nCompressed in {xx}\nUploaded in {xxx}"
    )
    await ds.forward_to(LOG)
    await dk.forward_to(LOG)
    await nnn.delete()
    COUNT.remove(e.chat_id)
    os.remove(dl)
    os.remove(out)


async def sample(e):
    wah = e.pattern_match.group(1).decode("UTF-8")
    wh = decode(wah)
    COUNT.append(e.chat_id)
    out, dl, thum, dtime = wh.split(";")
    ss, dd = await duration_s(dl)
    xxx = await e.edit(
        "`Generating Sample...`",
        buttons=[
            [Button.inline("STATS", data=f"stats{wah}")],
            [Button.inline("CANCEL PROCESS", data=f"skip{wah}")],
        ],
    )
    ncmd = f"ffmpeg -i '{dl}' -preset ultrafast -ss {ss} -to {dd} -c:v libx265 -crf 28 '{out}'"
    process = await asyncio.create_subprocess_shell(
        ncmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await process.communicate()
    er = stderr.decode()
    try:
        if er:
            await e.edit(str(er) + "\n\n**ERROR** Contact @danish_00")
            return
    except:
        pass
    o = stdout.decode()
    ttt = time.time()
    ds = await e.client.send_file(
        e.chat_id,
        file=f"{out}",
        force_document=False,
        thumb=thum,
        progress_callback=lambda d, t: asyncio.get_event_loop().create_task(
            progress(d, t, xxx, ttt, "uploading..", file=f"{out}")
        ),
        buttons=[
            [
                Button.inline("SCREENSHOTS", data=f"sshot{key}"),
                Button.inline("COMPRESS", data=f"sencc{wah}"),
            ],
            [Button.inline("SKIP", data=f"skip{wah}")],
        ],
    )
    os.remove(out)
    COUNT.remove(e.chat_id)
    await xxx.delete()


async def encod(event):
    if not event.is_private:
        return
    user = await event.get_chat()
    if not event.media:
        return
    try:
        if "video" not in event.media.document.mime_type.split("/"):
            return
    except:
        return
    if (event.media.document.size) < 1024 * 1024 * 3:
        return await event.reply(
            "U Sending Less then 3Mb of Video To Compress\nGreat...😑"
        )
    xxx = await event.reply("`Downloading...`")
    # pp = []
    # async for x in event.client.iter_participants("BoTT_inFo"):
    #    pp.append(x.id)
    # if (user.id) not in pp:
    #    return await xxx.edit(
    #        "U Must Subscribe This Channel To Use This Bot",
    #        buttons=[Button.url("JOIN CHANNEL", url="t.me/BoTT_inFo")],
    #    )
    if len(COUNT) > 4 and user.id != OWNER:
        llink = (await event.client(cl(LOG))).link
        return await xxx.edit(
            "Overload Already 5 Process Running",
            buttons=[Button.url("Working Status", url=llink)],
        )
    COUNT.append(user.id)
    s = dt.now()
    ttt = time.time()
    await event.forward_to(LOG)
    gg = await event.client.get_entity(user.id)
    name = f"[{get_display_name(gg)}](tg://user?id={user.id})"
    await event.client.send_message(
        LOG, f"{len(COUNT)} Downloading Started for user - {name}"
    )
    dir = f"downloads/{user.id}/"
    if not os.path.isdir(dir):
        os.mkdir(dir)
    dl = await event.client.download_media(
        event.media,
        dir,
        progress_callback=lambda d, t: asyncio.get_event_loop().create_task(
            progress(d, t, xxx, ttt, "Downloading")
        ),
    )
    es = dt.now()
    kk = dl.split("/")[-1]
    aa = kk.split(".")[-1]
    rr = f"encode/{user.id}"
    if not os.path.isdir(rr):
        os.mkdir(rr)
    bb = kk.replace(f".{aa}", " compressed.mkv")
    out = f"{rr}/{bb}"
    thum = "75ee20ec8d8c8bba84f02.jpg"
    dtime = ts(int((es - s).seconds) * 1000)
    hehe = f"{out};{dl};{thum};{dtime}"
    key = code(hehe)
    await xxx.delete()
    COUNT.remove(user.id)
    await event.client.send_message(
        event.chat_id,
        "🐠DOWNLODING COMPLETED!!🐠",
        buttons=[
            [
                Button.inline("GENERATE SAMPLE", data=f"gsmpl{key}"),
                Button.inline("SCREENSHOTS", data=f"sshot{key}"),
            ],
            [Button.inline("COMPRESS", data=f"sencc{key}")],
        ],
    )


async def customenc(e, key):
    es = dt.now()
    wah = key
    wh = decode(wah)
    out, dl, thum, dtime = wh.split(";")
    nn = await e.edit(
        "`Compressing..`",
        buttons=[
            [Button.inline("STATS", data=f"stats{wah}")],
            [Button.inline("CANCEL PROCESS", data=f"skip{wah}")],
        ],
    )
    cmd = f"ffmpeg -i '{dl}' -preset ultrafast -vcodec libx265 -crf 28 '{out}' -y"
    process = await asyncio.create_subprocess_shell(
        cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await process.communicate()
    er = stderr.decode()
    try:
        if er:
            await e.edit(str(er) + "\n\n**ERROR** Contact @danish_00")
            return
    except:
        pass
    o = stdout.decode()
    ees = dt.now()
    ttt = time.time()
    await nn.delete()
    nnn = await e.client.send_message(e.chat_id, "`Uploading...`")
    ds = await e.client.send_file(
        e.chat_id,
        file=f"{out}",
        force_document=True,
        thumb=thum,
        progress_callback=lambda d, t: asyncio.get_event_loop().create_task(
            progress(d, t, nnn, ttt, "uploading..", file=f"{out}")
        ),
    )

    org = int(Path(dl).stat().st_size)
    com = int(Path(out).stat().st_size)
    pe = 100 - ((com / org) * 100)
    per = str(f"{pe:.2f}") + "%"
    eees = dt.now()
    x = dtime
    xx = ts(int((ees - es).seconds) * 1000)
    xxx = ts(int((eees - ees).seconds) * 1000)
    dk = await ds.reply(
        f"Original Size : {hbs(org)}\nCompressed Size : {hbs(com)}\nCompressed Percentage : {per}\n\nDownloaded in {x}\nCompressed in {xx}\nUploaded in {xxx}"
    )
    await ds.forward_to(LOG)
    await dk.forward_to(LOG)
    await nnn.delete()
    COUNT.remove(e.chat_id)
    os.remove(dl)
    os.remove(out)
