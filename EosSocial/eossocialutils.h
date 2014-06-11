#ifndef __EOS_SOCIAL_UTILS_H__
#define __EOS_SOCIAL_UTILS_H__

#include <webkit2/webkit2.h>

typedef struct {
  WebKitWebView parent;
} EosSocialWebView;

typedef struct {
  WebKitWebViewClass parent_class;
} EosSocialWebViewClass;

void eos_social_web_view_setup (EosSocialWebView *self);
GType eos_social_web_view_get_type (void);

#endif /* __EOS_SOCIAL_UTILS_H__ */
