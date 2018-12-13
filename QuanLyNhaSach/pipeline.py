from QuanLyNhaSach.models.user_profile import Profile


def get_avatar(backend, strategy, details, response,
               user=None, *args, **kwargs):
    url = None
    display_name = ""
    if backend.name == 'google-oauth2':
        url = response['image'].get('url')
        display_name = response['displayName']
        ext = url.split('.')[-1]
    if url:
        profile = Profile.objects.filter(user_id=user.id)
        if profile.count() == 0:
            ins = Profile(avatar=url, user=user, display_name=display_name)
            ins.save()
        else:
            ins = profile[0]
            ins.avatar = url
            ins.display_name = display_name
            ins.save()
