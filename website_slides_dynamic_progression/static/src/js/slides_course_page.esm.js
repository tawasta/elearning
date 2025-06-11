/** @odoo-module **/

import publicWidget from '@web/legacy/js/public/public_widget';
import { SlideCoursePage } from '@website_slides/js/slides_course_page';

SlideCoursePage.include({
    async _toggleSlideCompleted(slide, completed = true) {
        await this._super(slide, completed);
        this._refreshSlidesList();
    },

    _refreshSlidesList() {
        const $wrapper = $('.mb-5.o_wslides_slides_list');
        if (!$wrapper.length) {
            console.warn('SlideCoursePage: .o_wslides_slides_list_wrapper ei löytynyt.');
            return;
        }

        $.get(window.location.href, (data) => {
            const updatedContent = $(data).find('.mb-5.o_wslides_slides_list').html();
            if (updatedContent) {
                $wrapper.html(updatedContent);
            }
        });
    }
});
