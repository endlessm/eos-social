#include <string.h>

#include "eossocialutils.h"

enum {
  LOAD_FAILED_2,
  LAST_SIGNAL
};
static guint signals[LAST_SIGNAL] = { 0, };

G_DEFINE_TYPE (EosSocialWebView, eos_social_web_view, WEBKIT_TYPE_WEB_VIEW)

static void
eos_social_web_view_class_init (EosSocialWebViewClass *klass)
{
  signals[LOAD_FAILED_2] = g_signal_new ("load-failed-2",
                                         eos_social_web_view_get_type (),
                                         G_SIGNAL_RUN_LAST,
                                         0, NULL, NULL, NULL,
                                         G_TYPE_BOOLEAN,
                                         3,
                                         WEBKIT_TYPE_LOAD_EVENT,
                                         G_TYPE_STRING,
                                         G_TYPE_ERROR);
}

static gboolean
on_load_failed (WebKitWebView *web_view,
                WebKitLoadEvent load_event,
                gchar *failing_uri,
                GError *error,
                gpointer user_data)
{
  gboolean res = FALSE;

  g_signal_emit (web_view, signals[LOAD_FAILED_2], 0,
                 load_event, failing_uri, error,
                 &res);

  return res;
}

void
eos_social_web_view_setup (EosSocialWebView *self)
{
  gchar *cpu, *tail = NULL, *ua = NULL;
  WebKitSettings *settings = webkit_web_view_get_settings (WEBKIT_WEB_VIEW (self));

  g_object_get (G_OBJECT (settings), "user-agent", &ua, NULL);
  if (ua)
    tail = strstr (ua, "AppleWebKit");

  if (!tail)
    tail = "AppleWebKit/538.1 (KHTML, like Gecko) Safari/538.1";

#if defined(__i386__)
  cpu = "i586";
#elif defined(__x86_64__)
  cpu = "x86_64";
#elif defined(__arm__)
  cpu = "armv7l";
#else
  cpu = "unknown";
#endif

  /* Temporary workaround: adding this bit to the user-agent makes Facebook format
   * external links in a way that correctly triggers a new browser window when clicked.
   * https://github.com/endlessm/eos-shell/issues/2765
   */
  gchar* extra = "Chrome/33";

  gchar *nua = g_strdup_printf ("Mozilla/5.0 (X11; Linux %s) %s %s", cpu, tail, extra);
  g_object_set (G_OBJECT (settings), "user-agent", nua, NULL);

  g_free (nua);
  g_free (ua);
}

static void
eos_social_web_view_init (EosSocialWebView *self)
{
  g_signal_connect (self, "load-failed",
                    G_CALLBACK (on_load_failed), NULL);
}

