#ifndef __EOS_SOCIAL_UTILS_H__
#define __EOS_SOCIAL_UTILS_H__

#include <webkit2/webkit2.h>

typedef void (* EosSocialLoadFailedCallback) (WebKitWebView *web_view,
                                              WebKitLoadEvent load_event,
                                              const gchar *failing_uri,
                                              const GError *error,
                                              gpointer user_data);

void eos_social_connect_to_load_failed (WebKitWebView *web_view,
                                        EosSocialLoadFailedCallback callback,
                                        gpointer user_data);

#endif /* __EOS_SOCIAL_UTILS_H__ */
