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

static void
eos_social_web_view_init (EosSocialWebView *self)
{
  g_signal_connect (self, "load-failed",
                    G_CALLBACK (on_load_failed), NULL);
}

